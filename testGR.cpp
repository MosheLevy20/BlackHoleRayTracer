#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include "chrisC.h"
#include "Ray.h"
#include "Vector3.h"
#include "omp.h"
using namespace std;

//cartersian to spherical in physics notation
Vector3 cart2sph(Vector3 v){
    double r = v.magnitude();
    double theta = acos(v.getZ()/r);
    double phi = atan2(v.getY(), v.getX());
    
    return Vector3(r,theta,phi);
}


int main()
{
    //get the christoffel symbols from python script
    // system("python3 GR_RayTracer2D.py");
    float fov = M_PI/2;
    float tf2 = tan(fov/32);
    //black hole mass
    float M = 1;
    //black hole radius (event horizon)
    float R = 2*M;

    float t = 0;
    //generate rays 
    //camera position in cartesian coordinates
    Vector3 camPos = Vector3(0,0,20*R);
    //camera direction in cartesian coordinates
    Vector3 camDir = Vector3(0,0,-1);
    //normalize camera direction
    camDir.normalize();
    
    //first get two vectors that are perpendicular to the camera direction
    Vector3 perp1 = Vector3(0, 1, 0);
    Vector3 perp2 = camDir.cross(perp1);
    //normalize the perpendicular vectors
    perp1.normalize();
    perp2.normalize();

    //convert camera direction to spherical coordinates
    // camDir = cart2sph(camDir);
    // //convert the perpendicular vectors to spherical coordinates
    // perp1 = cart2sph(perp1);
    // perp2 = cart2sph(perp2);
    camDir.print();

    Vector3 rayPosSph = cart2sph(camPos);
    cout<<"this<<"<<endl;
    rayPosSph.print();
  
    //generate rays and draw image
    ofstream myfile("para.txt");
    //open file and remove old data
    //png header
    float xres = 128;
    float yres = 128;
    int Ixres = (int)xres;
    int count = 0;
    myfile << xres << " " << yres << endl;
    #pragma omp parallel for
    for (int i=0; i < Ixres; i++)
    {
        
        for (int j =0; j < yres; j++)
        {
            //generate ray
            //ray position = camera position
            
            
            //get ray direction in cartesian coordinates
            //Vector3 rayDirSph = camDir + perp1*((i - xres/2)/xres)*0.1 + perp2*((j - yres/2)/yres)*0.1;
            //normalize ray direction
            //rayDirSph.normalize();
            //rayDirSph *= 0.000;

            //convert ray direction to spherical coordinates
            //rayDirSph = cart2sph(rayDirSph);
            //convert ray position to spherical coordinates
            //rayDirSph.print();
            //get array from vector3
            //float rayPosArr[4] = {t ,rayPosSph.getX(), rayPosSph.getY(), rayPosSph.getZ()};
            // float rayPosArr[4] = {t ,15*R, 0.1, M_PI/2};
            // float a = 0.06*(i-xres/2)/xres/4;
            // float b = 0.06*(j-yres/2)/yres;
            // float rayDirArr[4] = {1 ,0.01,a,b};
        
            float r0= 13*R;
            float theta0 = M_PI/2.1;
            float phi0 = 0.0;
            float rho = 1;//aspect ratio
            //4 vec array k
            float k[4] = {-1,-1,rho*((2*i/xres-1))*tf2, (1-2*j/yres)*tf2};
            float rayPosArr[4] = {0 ,r0, theta0, phi0};
            // 	norm = math.sqrt(k[1]**2+k[2]**2)
            // 	k[1] /= norm
            // 	k[2] /= norm
            
            Ray ray(rayPosArr, k);
            //while ray is not in the black hole and not too far away
            //cout << "ray r: " << ray.getR() << endl;
            int steps = 0;
            while (ray.getR() > 1.05*R && ray.getR() < 100*R)
            {
                ray.geodesic();
                //cout << "ray r 2: " << ray.getR() << endl;
                //if ray is in accretion disk
                float rr = ray.getR();
                float theta = ray.getTheta();
                if (abs(theta- M_PI/2)<0.01  && rr<7*R && rr > 1.05*R)
                {
                     
                    //cout<<"hit accretion disk "<< 255*1.05*R/rr<<endl;
                    //draw pixel red, brightness is a function of distance from black hole
                    myfile << (int)(255*1.05*R/rr) << " " << 0 << " " << 0 <<" " << i << " " << j << endl;
                    //myfile << 255 << " " << 0 << " " << 0 << " " << endl;
                    break;
                }
                

               
                //cout ray pos
                //cout << "ray pos: " << ray.getR() << " " << ray.getTheta() << " " << ray.getPhi() << endl;
                //cout ray dir
                //cout << "ray dir: " << ray.getVr() << " " << ray.getVtheta() << " " << ray.getVphi() << endl;
                //break;
                steps++;
                if (steps > 50000)
                {
                    //draw pixel black
                     myfile << "0 0 0 "<<" " << i << " " << j << endl;
                    break;
                }
            
            }
            if (abs(ray.getR()) < 1.05*R)
            {
                //draw pixel black
                //cout<<"hit black hole"<<endl;
                myfile << "0 0 0 "<<" " << i << " " << j << endl;
            }
            else if (ray.getR() > 100*R)
            {
                //draw pixel white
                //cout<<"missed"<<endl;
                myfile << "0 0 0 "<<" " << i << " " << j << endl;
            }
        
            
                 
            //get ray color
            //if ray is in the black hole or too far away
            
            //if last pixel in row and column
            
            
        }
    //print progress
    count += 1;
    cout << "progress: " << count/(float)xres << endl;
       
    }
    myfile.close();

    

    return 0;
}

//to compile with openmp support:g++ -fopenmp -o testGR testGR.cpp chrisC.cpp Ray.cpp Vector3.cpp -std=c++11
