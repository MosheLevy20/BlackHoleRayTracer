//implementation of the Vector3 class
//include standard libraries
#include <iostream>
#include <cmath>

#include "Vector3.h"

//constructors
Vector3::Vector3() {
    x = 0;
    y = 0;
    z = 0;
}
Vector3::Vector3(float x, float y, float z) : x(x), y(y), z(z) {}

Vector3::Vector3(const Vector3& v){
    //copy Vector3 from another
    x = v.getX();
    y = v.getY();
    z = v.getZ();
}


//destructor
Vector3::~Vector3() {}

//getters
float Vector3::getX() const {
    return x;
}
float Vector3::getY() const {
    return y;
}
float Vector3::getZ() const {
    return z;
}
//setters
void Vector3::setX(float x) {
    this->x = x;
}
void Vector3::setY(float y) {
    this->y = y;
}
void Vector3::setZ(float z) {
    this->z = z;
}
//overloaded operators
//addition
Vector3 Vector3::operator+(const Vector3& v) const {
    return Vector3(x + v.getX(), y + v.getY(), z + v.getZ());
}
//subtraction
Vector3 Vector3::operator-(const Vector3& v) const {
    return Vector3(x - v.getX(), y - v.getY(), z - v.getZ());
}
//scalar multiplication
Vector3 Vector3::operator*(float scalar) const {
    return Vector3(x * scalar, y * scalar, z * scalar);
}
//scalar division
Vector3 Vector3::operator/(float scalar) const {
    return Vector3(x / scalar, y / scalar, z / scalar);
}
//assignment
Vector3& Vector3::operator=(const Vector3& v) {
    x = v.getX();
    y = v.getY();
    z = v.getZ();
    return *this;
}
//addition assignment
Vector3& Vector3::operator+=(const Vector3& v) {
    x += v.getX();
    y += v.getY();
    z += v.getZ();
    return *this;
}   
//subtraction assignment
Vector3& Vector3::operator-=(const Vector3& v) {
    x -= v.getX();
    y -= v.getY();
    z -= v.getZ();
    return *this;
}
//scalar multiplication assignment
Vector3& Vector3::operator*=(float scalar) {
    x *= scalar;
    y *= scalar;
    z *= scalar;
    return *this;
}
//scalar division assignment
Vector3& Vector3::operator/=(float scalar) {
    x /= scalar;
    y /= scalar;
    z /= scalar;
    return *this;
}

//dot product
float Vector3::dot(const Vector3& v) const {
    return x * v.getX() + y * v.getY() + z * v.getZ();
}
//cross product
Vector3 Vector3::cross(const Vector3& v) const {
    return Vector3(y * v.getZ() - z * v.getY(), z * v.getX() - x * v.getZ(), x * v.getY() - y * v.getX());
}
//magnitude
float Vector3::magnitude() const {
    return sqrt(x * x + y * y + z * z);
}
//magnitude squared
float Vector3::magnitudeSquared() const {
    return x * x + y * y + z * z;
}
//normalize
void Vector3::normalize() {
    float mag = magnitude();
    x /= mag;
    y /= mag;
    z /= mag;
}
//print
void Vector3::print() const {
    std::cout << "(" << x << ", " << y << ", " << z << ")" << std::endl;
}
