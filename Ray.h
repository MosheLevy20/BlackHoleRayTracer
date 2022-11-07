//header for Ray class
#ifndef RAY_H
#define RAY_H

#include <iostream>
#include <cmath>
#include <vector>
#include "chrisC.h"

using namespace std;

class Ray{

private:
    double pos[4];
    double vel[4];
    vector<vector<double>> worldLine;

public:
    Ray();
    Ray(double pos[4], double vel[4]);
    //destructor
    ~Ray();
    //getters
    double getR();
    double getTheta();
    double getPhi();
    double getT();
    double getVr();
    double getVtheta();
    double getVphi();
    double getVt();
    
    vector<vector<double>> getWorldLine();

    void geodesic();

};


#endif