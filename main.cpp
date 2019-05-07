#include <opencv2/highgui/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <stdlib.h>
#include <iostream>

int
main(int argc, char *argv[])
{
    double ellipse_center_x;
    double ellipse_center_y;//楕円の中心座標の初期位置
    double angle;//楕円の初期角度
    double ellipse_length;
    int num1;
    int num2;
    
    ellipse_center_x = 500;
    ellipse_center_y = 500;
    angle = 0;
    ellipse_length = 20;
    
    for (int i = 0 ; i < 100000 ; i++) {
        cv::Mat img = cv::Mat::zeros(1000, 1000, CV_8UC3);
        
        if(ellipse_center_x < 100 || ellipse_center_x > 900 || ellipse_center_y < 100 || ellipse_center_y > 900){
            
            while (ellipse_center_x < 100 || ellipse_center_x > 900 || ellipse_center_y < 100 || ellipse_center_y > 900) {
                //フレームから出そうになった時に方向転換する
                num2 = rand() % 3;//0,1,2,の中からランダムに数字を取る
                angle = angle + 180 + (num2 - 1) * 30 ;
                ellipse_center_x = ellipse_center_x - 10 * cos(angle * 3.141592 / 180);
                ellipse_center_y = ellipse_center_y - 10 * sin(angle * 3.141592 / 180);
            }
            
        }
        
        
        else{
            num1 = rand() % 7;//0,1,2,3,4,5,6の中からランダムに数字を取る
            angle = angle + (num1 - 3) * 10;
        
            ellipse_center_x = ellipse_center_x - 10 * cos(angle * 3.141592 / 180);
            ellipse_center_y = ellipse_center_y - 10 * sin(angle * 3.141592 / 180);//ランダムで方向転換しながら進む
            
        }
        
        cv::ellipse(img, cv::Point(ellipse_center_x, ellipse_center_y), cv::Size(ellipse_length, 10), angle, 0, 360, cv::Scalar(200,0,0), -1, 3);
        
        double connect_point_x;
        double connect_point_y;
        
        connect_point_x = ellipse_center_x + ellipse_length * cos(angle * 3.141592 / 180);
        connect_point_y = ellipse_center_y + ellipse_length * sin(angle * 3.141592 / 180);
        //魚の胴体と尾っぽの部分のつなぎ点
        
        cv::Point pt[3]; //任意の3点を配列に入れる
        pt[0] = cv::Point(connect_point_x, connect_point_y);
        pt[1] = cv::Point(connect_point_x + 15 * cos((angle + 45) * 3.141592 / 180), connect_point_y + 15 * sin((angle + 45) * 3.141592 / 180));
        pt[2] = cv::Point(connect_point_x + 15 * cos((angle - 45) * 3.141592 / 180), connect_point_y + 15 * sin((angle - 45) * 3.141592 / 180));
        //魚の尾っぽの部分
        
        cv::fillConvexPoly(img, pt, 3, cv::Scalar(200,0,0) );
        
        cv::namedWindow("drawing", cv::WINDOW_AUTOSIZE|cv::WINDOW_FREERATIO);
        cv::imshow("drawing", img);
        cv::waitKey(100);
        
    }
    return 0;
    
}
