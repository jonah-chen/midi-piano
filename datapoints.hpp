#pragma once
/* This file will contain all the datapoints required for the webcam */

#include <iostream>
#include <string>
#include <vector>

struct note
{
    std::string name;
    int webcam, x, y, r;
    note(const std::string&, int, int, int = 0, int = 3);
    friend std::ostream& operator<<(std::ostream& os, const note& note)
    {
        os << note.name << " at (" << note.x << "," << note.y << ")\n";
        return os;
    }
};

class Stream
{
    std::vector<note> notes;
    int id;
public:
    Stream(int);
    void operator+=(const note& note) {notes.push_back(note); }
};



