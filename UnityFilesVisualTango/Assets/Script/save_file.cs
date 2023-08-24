using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System;
using UnityEngine;
using System.IO;
using System.Text;
using UnityEngine.UI;
using SFB;
using System.Runtime.InteropServices; // Add this line
using static System.Math;
public class save_file : MonoBehaviour
{
    [DllImport("__Internal")]
    private static extern void DownloadFile(string gameObjectName,string methodName,string filename,byte[] byteArray,int byteArraySize);
    
    
    List<int> angle = new List<int>(){ 0, 30, 60, 90, 120, 150, 180, 270, 360 };

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Awake()
    {
        Button button = gameObject.GetComponent<Button>() as Button;
        button.onClick.AddListener(Save);
    }
    
    public void Save()
    {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < streaming.l.Count; i++)
        {
            sb.Append(streaming.l[i].p);
            sb.Append(streaming.l[i].h);
            sb.Append(streaming.l[i].w);
            sb.Append(streaming.l[i].d);
            sb.Append(streaming.l[i].t);
            if (streaming.l[i].r < 0){
                sb.Append("1");
            } else {
                sb.Append("0");
            }
            int abs_angle = Math.Abs(streaming.l[i].r);
            int index = angle.Select((elem, index) => new {elem, index})
                        .First(p => p.elem == abs_angle)
                        .index;
            sb.Append(index);
            sb.Append(streaming.l[i].lean);
        }

        byte[] bytes = new UTF8Encoding().GetBytes(sb.ToString());
        DownloadFile(gameObject.name,"OnFileDownload","save.txt",bytes,bytes.Length);

        //var path = EditorUtility.SaveFolderPanel("Choose a local folder to save", "", "");
        
    }
    public void OnFileDownload(){}
    //+ DateTime.Now.GetDateTimeFormats('s')[0]
}
