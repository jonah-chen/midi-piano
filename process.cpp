/* This is intended to be program used to process the videos and outputs all the necessary information in the file. 
 * 
 * Two command line arguments (argc=3):
 *      1. input file path
 *      2. output file path
 */

#include <fstream>
#include <iostream>

#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>

/* Sum Kernal.
 * Objective: Find the sum of the kernal around the position (xp, yp) in the grayscale image of radius r.
 * Handled Exceptions: If any of the following conditions are not met, the function will throw an exception.
 *      r must be positive. 
 *      The entire kernal must exist within the image.
 * Unhandled Exceptions: These requirements must be met otherwise the function will have undefined behavior.
 *      Image MUST be in grayscale.
 * Runtime: Quadratic in the radius.
 */

int sum_ker(const cv::Mat& im,
            const int xp, const int yp, const int r=3)
{
    if (xp < r or yp < r or r <= 0)
        throw "your center is too close to the edge";
    
    int sum{};
    for (int i{-r}; i < r; ++i)
        for (int j{-r}; j < r; ++j)
            sum += im.data[(xp + i) * im.rows + (yp + j)];
    return sum;
}


/* Difference Kernal.
 * Objective: Find the sum of the differences around the position (xp, yp) in the grayscale image of radius r between the previous and current frame.
 * Handled Exceptions: If any of the following conditions are not met, the function will throw an exception.
 *      r must be positive. 
 *      The entire kernal must exist within the image.
 * Unhandled Exceptions: These requirements must be met otherwise the function will have undefined behavior
 *      BOTH images MUST be in grayscale
 * Runtime: Quadratic in the radius.
 */
double diff_ker(const cv::Mat& prev, const cv::Mat& cur,
                const int xp, const int yp, const int r=3,
                bool normalized=true)
{
    if (xp < r or yp < r or r <= 0)
        throw "your center is too close to the edge";
    double sum{}, p, c;
    for (int i{-r}; i < r; ++i)
    {
        for (int j{-r}; j < r; ++j)
        {
            p = (double)prev.data[(xp + i) * prev.rows + (yp + j)];
            c = (double)cur.data[(xp + i) * cur.rows + (yp + j)];
            sum += (p - c)/(c + 1.0);
        }
    }
    return sum / (r*r);
}


int main(int argc, char** argv)
{
    if (argc != 3)
    {
        std::cout << "Two arguments are not provided. Exited with error code 7.\n";
        exit(7);
    }

    std::ios_base::sync_with_stdio(false);
    
    cv::Mat frame, bw, prev;
    cv::VideoCapture cap(argv[1]);
    std::ofstream out(argv[2]);
    
    out << "FIRST LINE IS DESCRIPTION\n"; // write the head of the file

    cap >> frame;
    cv::cvtColor(frame, prev, cv::COLOR_BGR2GRAY);

    while (true)
    {
        cap >> frame;
        if (frame.empty())
            break;
        cv::cvtColor(frame, bw, cv::COLOR_BGR2GRAY);

        out << diff_ker(prev, bw, 100, 100) << " ";
        out << diff_ker(prev, bw, 50, 80) << " ";

        cv::imshow("img", frame);

        if ((char)cv::waitKey(1) == 'q')
            break;
        
        out << "\n"; // end of frame
    }
    
    return 0;
}
