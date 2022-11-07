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
    float pos[4];
    float vel[4];
    vector<vector<float>> worldLine;

public:
    Ray();
    Ray(float pos[4], float vel[4]);
    //destructor
    ~Ray();
    //getters
    float getR();
    float getTheta();
    float getPhi();
    float getT();
    float getVr();
    float getVtheta();
    float getVphi();
    float getVt();
    
    vector<vector<float>> getWorldLine();

    void geodesic();

};


#endif