/*
   compilation command:
   g++ -std=c++11 reader.cpp -o reader
 */

#include <iostream>
#include <iomanip>
#include <fstream>
#include <cstdint>
#include <vector>
using namespace std;

struct RECORD
{
    uint64_t hits;
    uint64_t time;
};

double unitVolt(int unitArb)
{
    double result;
    result = (double)(unitArb*10)/4095;
    return result;
}

int main()
{
    string prefix = "scan-hv";

    string name;
    int i, n, size,hv,th, event, layer, strip;
    struct RECORD buffer;
    ofstream outfile;
    outfile.open("plot.txt");
    // open file


    int numberOfEvent;
    vector <int>collection(64);
    vector <int> ns(4);


    for(hv=2400; hv<=3400;hv+=50){

        for(th=90;th<=140;th+=5){


            name = prefix + to_string(hv) + "-th" + to_string(th)+".dat";
            cout << "file " << name << endl;
            ifstream infile(name, ios::binary | ios::in);

            if(!infile.is_open())
            {
                cerr << "cannot open file " << name << endl;
                continue;
            }

            // get file size
            infile.seekg (0, ios::end);
            size = infile.tellg();
            infile.seekg (0, ios::beg);
            cout << "file size " << size << endl;
            // calculate number of events because one event is 16 char
            n = size / 16;

            int ne=0;
            int numberOfStrip;
            numberOfEvent=0;
            // read all events
            for(event = 0; event < n; event += 1)
            {
                // read event
                infile.read((char *) &buffer, 16);

                // print event
                ios::fmtflags flags(cout.flags());
                cout << setfill(' ') << setw(8) << dec << event << " "; //rempli avec des espaces afin d'avoir 8caractères au total
                cout << setfill('0') << setw(16) << hex << buffer.time << " "; //rempli avec des 0 afin d'avoir 16 caractères au total.
                cout << setfill('0') << setw(16) << hex << buffer.hits << " ";
                cout.flags(flags);//sets some format flags for cout that affect the insertion operation

                    ns[0]=0;
                    ns[1]=0;
                    ns[2]=0;
                    ns[3]=0;

                numberOfStrip=0;
                // print layers and strips with hits
                for(i = 0; i < 64; i += 1)
                {
                    

                    if((buffer.hits >> i & 1) == 0) continue;
                    layer = i / 16;
                    strip = i % 16;
                    cout << layer << ":" << strip << " ";
                    ns[layer]+=1;
                    numberOfStrip+=1;
                    //if(strip>0 && strip<15) numberOfStrip+=1;



                }

                //collection[numberOfStrip]+=1;
                //outfile << numberOfStrip << endl;

                /*if (numberOfStrip<=12 && numberOfStrip>=4){
                    numberOfEvent+=1;
                }*/

                if (ns[0]<3 && ns[1]<3 && ns[2]<3 && ns[3]<3) ++ne;
                

                

            }

           outfile <<unitVolt(hv) << "  "<<th<<"   "<<ne<<endl;
        }

    }
    //for(i=0;i<64;i+=1){
    // outfile << i << "  "<< collection[i] << endl;}



    outfile.close(); 
    return 0;
}
