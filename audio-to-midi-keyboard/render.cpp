#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <vector>
#include <filesystem>

#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>

template <class T, class S, class C>
S& Container(std::priority_queue<T, S, C>& q) {
    struct HackedQueue : private std::priority_queue<T, S, C> {
        static S& Container(std::priority_queue<T, S, C>& q) {
            return q.*&HackedQueue::c;
        }
    };
    return HackedQueue::Container(q);
}

struct Note
{
    double start, end;
    int pitch;
    Note(double start, double end, int pitch)
    {
        this->start = start;
        this->end = end;
        this->pitch = pitch;
    }
    bool operator<(const Note& other) const { return end > other.end; }
    bool operator>(const Note& other) const { return start > other.start; }
};

class Sequence 
{
    static constexpr unsigned char ON = 0xff;

    unsigned char* video_buf; // this is the video sorted in row major order. 
    unsigned char* final_frame; // this is the last frame that is shown
    std::priority_queue<Note> cur_notes;
    std::vector<Note> &cur_notes_it = Container(cur_notes);
    
    int mapping[88], widths[88];
    int frame = 0;
    double scroll_time, tick_rate, tick;
    int frame_rate, x_res, y_res, last_frame;
    
    size_t position;

public:
    std::priority_queue<Note, std::vector<Note>, std::greater<Note>> seq; // bad practice, but I don't care

    Sequence(int length)
    {
        frame_rate = 24;
        x_res = 1080;
        y_res = 1920;
        scroll_time = 5;
        tick = 9.0;
        tick_rate = 5.0 / 1080.0;
        
        for (int i {}; i < 88; ++i)
        {
            mapping[i] = 21 * i;
            widths[i] = 18;
        }
        video_buf = new unsigned char[(size_t)(x_res*y_res*(2 + length/scroll_time))]();
        position = 0;
        last_frame = frame_rate * length;
    }

    ~Sequence()
    {
        // delete[] video_buf;
    }

    unsigned char* get_video_buf()
    {
        return video_buf;
    }

    unsigned char* get_cur_frame()
    {
        return final_frame;
    }
    void copy_first_frame(unsigned char* first_frame)
    {
        if (first_frame)
            std::memcpy(video_buf, first_frame, x_res*y_res);
    }

    unsigned char* next()
    {
        if (frame > last_frame)
            return nullptr;
        for (int t = frame * tick; t < frame * tick + tick; ++t)
        {
            double time = t * tick_rate;
            // If notes end before the tick, they are removed
            while (!cur_notes.empty() and cur_notes.top().end <= time)
                cur_notes.pop();
            // If notes start before the tick, they are added
            while (!seq.empty() and seq.top().start <= time)
            {
                cur_notes.push(seq.top());
                seq.pop();
            }

            // add the row to the image
            unsigned char *cur_row = video_buf + position + x_res*y_res;
            for (Note note : cur_notes_it)
                for (int offset = 0; offset < widths[note.pitch]; ++offset)
                    cur_row[mapping[note.pitch] + offset] = ON;

            position += y_res;
        }
        ++frame;
        final_frame = video_buf + position;
        return final_frame;
    }
};

int main(int argc, char **argv)
{
    std::ifstream input_file;
    cv::Mat frame; 
    unsigned char *tmp, *first_frame = nullptr, *video_buf = nullptr;
    char dummy;
    double start, end, len; 
    int pitch, i {};

    if (argc > 1)
        sleep(std::stoi(argv[1]));
    
    std::filesystem::current_path("/mnt/ramdisk");

    while (true)
    {
        tmp = (unsigned char*)0x1; // this is just a dummy address
        while (!input_file.is_open())
            input_file.open(std::to_string(i) + ".txt");
        
        input_file >> len;
        input_file >> dummy; // avoid errors on empty files

        Sequence v(len);
        v.copy_first_frame(first_frame);
        if (video_buf) delete[] video_buf;
        
        while (input_file.good())
        {
            input_file >> start;
            input_file >> end;
            input_file >> pitch;
            v.seq.push(Note(start, end, pitch));
        }
        input_file.close();
        std::filesystem::remove(std::to_string(i) + ".txt");

        // show videos like here. The file IO should be very fast.
        while(tmp)
        {
            tmp = v.next();
            if (!tmp)
                break;
            frame = cv::Mat(1080, 1920, CV_8U, tmp);
            cv::imshow("Image", frame);
            if ((char)cv::waitKey(45) == 'q')
                return 0;
        }
        first_frame = v.get_cur_frame();
        video_buf = v.get_video_buf();
        ++i;
    }
    return 0;
}