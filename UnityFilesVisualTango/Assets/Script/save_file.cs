﻿using System.Collections;
using System;
using UnityEngine;
using System.IO;
using System.Text;
using UnityEngine.UI;
using SFB;
using System.Runtime.InteropServices; // Add this line
public class save_file : MonoBehaviour
{
    [DllImport("__Internal")]
    private static extern void DownloadFile(string gameObjectName,string methodName,string filename,byte[] byteArray,int byteArraySize);
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
            sb.Append(streaming.l[i].d);
            sb.Append(streaming.l[i].h);
            sb.Append(streaming.l[i].p);
            sb.Append(streaming.l[i].r);
            sb.Append(streaming.l[i].t);
            sb.Append(streaming.l[i].w);
        }

        byte[] bytes = new UTF8Encoding().GetBytes(sb.ToString());
        DownloadFile(gameObject.name,"OnFileDownload","save.txt",bytes,bytes.Length);

        //var path = EditorUtility.SaveFolderPanel("Choose a local folder to save", "", "");
        
    }
    public void OnFileDownload(){}
    //+ DateTime.Now.GetDateTimeFormats('s')[0]
}
