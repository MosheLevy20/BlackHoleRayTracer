//Vector3 class header
#ifndef VECTOR3_H
#define VECTOR3_H

class Vector3 {
public:
    //constructors
    Vector3();
    Vector3(float x, float y, float z);
    Vector3(const Vector3& v);
    //destructor
    ~Vector3();
    //accessors
    float getX() const;
    float getY() const;
    float getZ() const;
    //mutators
    void setX(float x);
    void setY(float y);
    void setZ(float z);
    //overloaded operators
    Vector3 operator+(const Vector3& v) const;
    Vector3 operator-(const Vector3& v) const;
    Vector3 operator*(float scalar) const;
    Vector3 operator/(float scalar) const;
    Vector3& operator=(const Vector3& v);
    Vector3& operator+=(const Vector3& v);
    Vector3& operator-=(const Vector3& v);
    Vector3& operator*=(float scalar);
    Vector3& operator/=(float scalar);
    //other methods
    float dot(const Vector3& v) const;
    Vector3 cross(const Vector3& v) const;
    float magnitude() const;
    float magnitudeSquared() const;
    void normalize();
    void print() const;
private:
    float x;
    float y;
    float z;
};


#endif