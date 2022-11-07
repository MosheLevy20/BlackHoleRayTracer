//python version
// class ray(object):
// 	"""docstring for ray"""
// 	def __init__(self, pos, vel):
// 		self.pos = pos
// 		self.vel = vel
// 		self.worldLine = []
// 	def geodesic(self):
// 		self.worldLine.append(cartesian(self.pos))
		
// 		dim = len(self.pos)
// 		newVel = []
// 		for lamda, l in enumerate(self.vel):
// 			a = 0
// 			for mu in range(dim):
// 				for nu in range(dim):
// 					cVal = chrisC[lamda][mu][nu].subs(r, self.pos[1])
// 					a -= cVal*self.vel[mu]*self.vel[nu]
// 					//print(chrisC[0][0][1].subs(r, 3.5),'this')
// 			newVel.append(l+a*dTau)
// 		self.vel = newVel

// 		for lamda, l in enumerate(self.pos):
// 			self.pos[lamda] += self.vel[lamda]*dTau
//implementation in c++
#include "Ray.h"
#include "chrisC.h"
#include <iostream>
#include <cmath>
#include <vector>

//construnctor
Ray::Ray(){
    pos[0] = 0;
    pos[1] = 0;
    pos[2] = 0;
    pos[3] = 0;
    vel[0] = 0;
    vel[1] = 0;
    vel[2] = 0;
    vel[3] = 0;

}
//constructor with arguments
Ray::Ray(float pos[4], float vel[4]){
    //cout << "ray constructor" << endl;
    // << "pos: "<< pos[0] << " " << pos[1] << " " << pos[2] << " " << pos[3] << endl;
    this->pos[0] = pos[0];
    this->pos[1] = pos[1];
    this->pos[2] = pos[2];
    this->pos[3] = pos[3];
    this->vel[0] = vel[0];
    this->vel[1] = vel[1];
    this->vel[2] = vel[2];
    this->vel[3] = vel[3];

    worldLine = vector<vector<float>>(0);
}
//destructors
Ray::~Ray(){
    //cout << "ray destructor" << endl;
    worldLine.clear();
}

void Ray::geodesic(){
    float dTau = 0.05;
    float chrisC1[4][4][4];
    //cout<<"chris inputs: "<<pos[1]<<","<<pos[2]<<","<<pos[3]<<endl;
    calcChrisC(pos[1], pos[2], pos[3], pos[0], chrisC1);
    float newVel[4];
    for(int lamda = 0; lamda < 4; lamda++){
        float a = 0;
        for(int mu = 0; mu < 4; mu++){
            for(int nu = 0; nu < 4; nu++){
                float cVal = chrisC1[lamda][mu][nu];
                //cout<<"chrisC1["<<lamda<<"]["<<mu<<"]["<<nu<<"] = "<<cVal<<endl;
                a -= cVal*vel[mu]*vel[nu];
            }
        }
        newVel[lamda] = vel[lamda] + a*dTau;
    }
    for(int lamda = 0; lamda < 4; lamda++){
        vel[lamda] = newVel[lamda];
    }

    for(int lamda = 0; lamda < 4; lamda++){
        pos[lamda] += newVel[lamda]*dTau;
    }

    //define posVec
    vector<float> posVec;
    posVec.push_back(pos[0]);
    posVec.push_back(pos[1]);
    posVec.push_back(pos[2]);
    posVec.push_back(pos[3]);
    worldLine.push_back(posVec);
}




vector<vector<float>> Ray::getWorldLine(){
    return worldLine;
}


//getters
float Ray::getR(){
    return pos[1];
}
float Ray::getTheta(){
    return pos[2];
}
float Ray::getPhi(){
    return pos[3];
}
float Ray::getT(){
    return pos[0];
}
float Ray::getVr(){
    return vel[1];
}
float Ray::getVtheta(){
    return vel[2];
}
float Ray::getVphi(){
    return vel[3];
}
float Ray::getVt(){
    return vel[0];
}




