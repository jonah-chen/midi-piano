/* This is intended to be program used to process the videos and outputs all the necessary information in the file. 
 * 
 * Two command line arguments (argc=3):
 *      1. input file path
 *      2. output file path
 */

#include <fstream>
#include <iostream>
#include <string>
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>


class Note
{
    int x, y, r;
public:
    std::string name;
    Note(const std::string& name, int x, int y, int r = 3)
    {
        if (x < r or y < r or r <= 0)
            throw "your center is too close to the edge";
        this->name = name;
        this->x = x;
        this->y = y;
        this->r = r - 1;
    }
    ~Note() {}

    /* Overriden print operation */
    friend std::ostream& operator<<(std::ostream& os, const Note& note)
    {
        os << note.name << " at (" << note.x << "," << note.y << ")\n";
        return os;
    }

    /* Find the sum of the pixel values about this note of the image im. */
    int sum(const cv::Mat& im) const
    {
        int sum{};

        if (im.isContinuous())
            for (int i{-r}; i <= r; ++i)
                for (int j{-r}; j <= r; ++j)
                    sum += im.data[(x + i) * im.rows + (y + j)];
        else 
        {
            std::cout << "You are not continuous\n";
            unsigned char *sub;
            for (int i{-r}; i <= r; ++i)
            {
                sub = im.row(x + i).data;
                for (int j{-r}; j <= r; ++j)
                    sum += sub[y+j]; // the maximum brightness
            }
        }
        return sum;
    }

    /* Find the difference of the pixel values about this note of the image prev from the image cur. */
    double diff(const cv::Mat& prev, const cv::Mat& cur, bool normalized=true) const
    {
        double sum{}, p, c;
        if (prev.isContinuous() and cur.isContinuous())
        {
            for (int i{-r}; i <= r; ++i)
            {
                for (int j{-r}; j <= r; ++j)
                {
                    p = (double)prev.data[(x + i) * prev.cols + (y + j)];
                    c = (double)cur.data[(x + i) * cur.cols + (y + j)];
                    sum += (p - c)/((p > c ? p : c) + 1.0);
                }
            }
        }
        else 
        {
            std::cout << "You are not continuous\n";
            unsigned char *subp, *subc;
            for (int i{-r}; i <= r; ++i)
            {
                subp = prev.row(x + i).data;
                subc = cur.row(x + i).data;
                for (int j{-r}; j <= r; ++j)
                {
                    p = (double)subp[y+j];
                    c = (double)subc[y+j];
                    sum += (p - c)/(c + 1.0);
                }
            }
        }
        return normalized ? sum / (r*r) : sum;
    }

    void display_region(const cv::Mat& im) const
    {
        if (im.isContinuous())
        {
            for (int i{-r}; i <= r; ++i)
                for (int j{-r}; j <= r; ++j)
                    im.data[(x + i) * im.cols + (y + j)] = 255u;
        }
        else
        {
            std::cout << "You are not continuous\n";
            unsigned char *sub;
            for (int i{-r}; i <= r; ++i)
            {
                sub = im.row(x + i).data;
                for (int j{-r}; j <= r; ++j)
                    sub[y+j] = 255u; // the maximum brightness
            }
        }
        
        cv::imshow(name, im);
        if ((char)cv::waitKey() == 'q')
            return;
    }
};

int main(int argc, char** argv)
{
    if (argc != 3)
    {
        std::cout << "Two arguments are not provided. Exited with error code 7.\n";
        exit(7);
    }

    std::ios_base::sync_with_stdio(false);
    
    cv::Mat frame, old[3], cur[3], tmp;
    cv::VideoCapture cap(argv[1]);
    std::ofstream out(argv[2]);

    Note notes[2] = {Note("test1", 200, 800, 5), Note("test2", 200, 850, 5)};
    // write the head of the file
    for (Note n : notes)
        out << n.name << ",";
    out.seekp(-1, std::ios_base::cur);
    out << "\n"; 

    cap >> frame;
    cv::GaussianBlur(frame, tmp, cv::Size(5,5), 0);
    cv::split(tmp, old);

    while (true)
    {
        cap >> frame;
        if (frame.empty())
            break;
        cv::GaussianBlur(frame, tmp, cv::Size(5,5), 0);
        cv::split(tmp, cur);

        for (Note n : notes)
            out << n.diff(old[0], cur[0]) + n.diff(old[1], cur[1]) + n.diff(old[2], cur[2]) << ",";
        out.seekp(-1, std::ios_base::cur);
        
        old[0] = cur[0].clone();
        old[1] = cur[1].clone();
        old[2] = cur[2].clone();

        out << "\n"; // end of frame
    }

    out.close();
    
    return 0;
}
