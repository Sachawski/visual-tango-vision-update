using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using OpenCvSharp;
using Mediapipe.Unity;
using Mediapipe.Unity.PoseTracking;

using MathNet.Numerics;
using MathNet.Numerics.LinearAlgebra;

using Google.Protobuf;


public class process_video : MonoBehaviour
{

    Dictionary<int,(int,int,int)> POSE_ARTICULATIONS = new Dictionary<int, (int, int, int)>
    {
        {23,(11,23,25)}, 
        {24,(12,24,26)}, 
        {25,(23,25,27)},
        {26,(24,26,28)}, 
        {27,(25,27,31)},
        {28,(26,28,32)}
    };

    Dictionary<int,(int,int,int)> COORDINATE_SYSTEM_INIT_DICT = new Dictionary<int, (int, int, int)>
    {
        {24,(12,24,23)},
        {23,(11,23,24)}
    };

    HashSet<int> ARTICULATIONS = new HashSet<int> {13,14,24,23,26,25,28,27};

    Dictionary<int,List<object>> coordinate_system = new Dictionary<int,List<object>>();

    // Start is called before the first frame update
    void Start()
    {
        //PoseTrackingGraph.LandmarkList.AddListener(OnLandmarksDetected);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    /*
    private void OnLandmarksDetected(LandmarkList landmarkList)
    {
        // Accédez aux landmarks individuels et effectuez des traitements supplémentaires
        for (int i = 0; i < landmarkList.Count; i++)
        {
            LandmarkList landmark = landmarkList[i];
            Vector3 landmarkPosition = new Vector3(landmark.X, landmark.Y, landmark.Z);

            // Faites quelque chose avec la position du landmark (par exemple, afficher un objet 3D à cet emplacement)
            // ...
        }
    }

    public List<object> coordinate_system_initialisation(Matrix<double> lmList,int articulation){
        if ((articulation == 24) | (articulation == 23)){
            
            int p1 = COORDINATE_SYSTEM_INIT_DICT[articulation].Item1;
            int p2 = COORDINATE_SYSTEM_INIT_DICT[articulation].Item2;
            int p3 = COORDINATE_SYSTEM_INIT_DICT[articulation].Item3;

            Vector<double> O = Vector<double>.Build.DenseOfArray(new double[] {lmList[p2,0],lmList[p2,1],lmList[p2,2]});
            Vector<double> OY = Vector<double>.Build.DenseOfArray(new double[] {lmList[p1,0],lmList[p1,1],lmList[p1,2]}) - O;

            if (OY.L2Norm() !=0)
                OY = OY / OY.L2Norm();
            Vector<double> temp = O - Vector<double>.Build.DenseOfArray(new double[] {lmList[p3,0],lmList[p3,1],lmList[p3,2]});



            Vector<double> OZ = Vector<double>.Build.DenseOfArray(new double[] {temp[1] * OY[2] - temp[2] * OY[1],
                                                                                temp[2] * OY[0] - temp[0] * OY[2],
                                                                                temp[0] * OY[1] - temp[1] * OY[0]});
            if (OZ.L2Norm() !=0)
                OZ = OZ / OZ.L2Norm();
            

            Vector<double> OX = Vector<double>.Build.DenseOfArray(new double[] {OY[1] * OZ[2] - OY[2] * OZ[1],
                                                                                OY[2] * OZ[0] - OY[0] * OZ[2],
                                                                                OY[0] * OZ[1] - OY[1] * OZ[0]});
            if (OX.L2Norm() !=0)
                OX = OX / OX.L2Norm();

            Matrix<double> P = Matrix<double>.Build.DenseOfArray(new double[,] {{ OX[0],OY[0],OZ[0] },
                                                                                { OX[1],OY[1],OZ[1] },
                                                                                { OX[2],OY[2],OZ[2] }});

            List<object> res = new List<object>();
            res.Add((object)O);
            res.Add((object)OX);
            res.Add((object)OY);
            res.Add((object)OZ);
            res.Add((object)P);
            return res; 
       
        } else {
            int p1 = POSE_ARTICULATIONS[articulation].Item1;
            int p2 = POSE_ARTICULATIONS[articulation].Item2;
            int p3 = POSE_ARTICULATIONS[articulation].Item3;

            Vector<double> O = Vector<double>.Build.DenseOfArray(new double[] {lmList[p2,0],lmList[p2,1],lmList[p2,2]});
            Vector<double> OY = Vector<double>.Build.DenseOfArray(new double[] {lmList[p1,0],lmList[p1,1],lmList[p1,2]}) - O;

            if (OY.L2Norm() !=0)
                OY = OY / OY.L2Norm();
            Vector<double> temp = O - Vector<double>.Build.DenseOfArray(new double[] {lmList[p3,0],lmList[p3,1],lmList[p3,2]});


            Vector<double> OX = Vector<double>.Build.DenseOfArray(new double[] {OY[1] * temp[2] - OY[2] * temp[1],
                                                                                OY[2] * temp[0] - OY[0] * temp[2],
                                                                                OY[0] * temp[1] - OY[1] * temp[0]});
            if (OX.L2Norm() !=0)
                OX = OX / OX.L2Norm();
            

            Vector<double> OZ = Vector<double>.Build.DenseOfArray(new double[] {OX[1] * OY[2] - OX[2] * OY[1],
                                                                                OX[2] * OY[0] - OX[0] * OY[2],
                                                                                OX[0] * OY[1] - OX[1] * OY[0]});
            if (OZ.L2Norm() !=0)
                OZ = OZ / OZ.L2Norm();


            Matrix<double> P = Matrix<double>.Build.DenseOfArray(new double[,] {{ OX[0],OY[0],OZ[0] },
                                                                                { OX[1],OY[1],OZ[1] },
                                                                                { OX[2],OY[2],OZ[2] }});
            List<object> res = new List<object>();
            res.Add((object)O);
            res.Add((object)OX);
            res.Add((object)OY);
            res.Add((object)OZ);
            res.Add((object)P);
            return res;                                                                    
        }
    }
    


    public Dictionary<string,double> angle(Matrix<double> lmList, int articulation, Dictionary<int,List<object>>coordinate_system){

        int p1 = POSE_ARTICULATIONS[articulation].Item1;
        int p2 = POSE_ARTICULATIONS[articulation].Item2;
        int p3 = POSE_ARTICULATIONS[articulation].Item3;

        //Points definition
        Vector<double> O = (Vector<double>)(coordinate_system[articulation])[0];
        Vector<double> A = (Vector<double>)lmList.Row(p1,0,3);
        Vector<double> B = (Vector<double>)lmList.Row(p2,0,3);
        Vector<double> C = (Vector<double>)lmList.Row(p3,0,3);
        Matrix<double> P = (Matrix<double>)coordinate_system[articulation][4];

        //Changing coordinate
        A = P*(A-O);
        B = P*(B-O);
        C = P*(C-O);

        //Calclating vectors
        Vector<double> AB = A - B;
        Vector<double> BC = B - C;

        //Vector normalisation
        if (AB.L2Norm() != 0)
            AB = AB / AB.L2Norm(); 
        if (BC.L2Norm() != 0)
            BC = BC / BC.L2Norm();
        
        // Euler angle calculaiton in the XY plan
        double angle_xy = System.Math.Atan2(BC[1], BC[0]) - System.Math.Atan2(AB[1], AB[0]);
        // Euler angle calculaiton in the XZ plan
        double angle_xz = System.Math.Atan2(BC[2], BC[0]) - System.Math.Atan2(AB[2], AB[0]);
        // Euler angle calculaiton in the YZ plan
        double angle_yz = System.Math.Atan2(BC[2], BC[1]) - System.Math.Atan2(AB[2], AB[1]);
        
        angle_xy = angle_xy * (180/System.Math.PI);
        if (angle_xy < 0)
            angle_xy += 360;
        if (angle_xy > 180)
            angle_xy -= 360;
        angle_xz = angle_xz * (180/System.Math.PI);
        if (angle_xz < 0)
            angle_xz += 360; 
        if (angle_xz > 180)
            angle_xz-= 360;
        angle_yz = angle_yz * (180/System.Math.PI);
        if (angle_yz < 0)
            angle_yz += 360; 
        if (angle_yz > 180)
            angle_yz -= 360;

        Dictionary<string,double> res = new Dictionary<string,double>  
        {
            {"x",angle_yz},
            {"y",angle_xz},
            {"z",angle_xy}
        };
        return res;
    } 
    
    public List<Dictionary<string,Dictionary<string,double>>> video_processing(){
        
        PoseTrackingGraph pose = new PoseTrackingGraph();
        bool process = true;
        VideoCapture video = new OpenCvSharp.VideoCapture();
        double width = video.Get(video.FrameWidth);
        double height = video.Get(video.FrameHeight);
        int n = 33;
        int frame = 0;
        List<Dictionary<string,Dictionary<string,double>>> all_angles = new List<Dictionary<string,Dictionary<string,double>>>();
        Dictionary<int,List<object>> coordinate_system = new Dictionary<int,List<object>>();

        while (process){
            OpenCvSharp.Mat imgMat = new OpenCvSharp.Mat();
            bool success = video.Read(imgMat);
            if (success){
                imgMat = imgMat.CvtColor(OpenCvSharp.ColorConversionCodes.BGR2RGB);
                
                ImageSource imgSrc = ImageSourceHelper.FromMat(imgMat);
                pose.StartRun(imgSrc);

                imgMat = imgMat.CvtColor(OpenCvSharp.ColorConversionCodes.RGB2BGR);
            }
        }
    }
    */




}
