using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.UI;
using UnityEngine;
using System;
using System.Globalization;
using System.Net.Http;
using System.IO;
using System.Text;
using System.Runtime.InteropServices; // Add this line
using UnityEngine.Networking;

public class animation : MonoBehaviour
{
    #if UNITY_WEBGL && !UNITY_EDITOR
    [DllImport("__Internal")]
    private static extern string GetURLFromPage();
    [DllImport("__Internal")]
    private static extern string GetIDFromPage();
    #endif


    
    public GameObject[] Body;
    List<string> lines = new List<string>();
    bool isPlaying = false;
    private Slider slider;
    private float tempSliderValue = 0;
    private bool tempPlayPauseStatus = false;
    //int counter = 0;
    private string url = "";
    private string id = "";

    void Awake()
    {
        #if UNITY_WEBGL && !UNITY_EDITOR
        id = GetIDFromPage();
        url = GetURLFromPage() + "/static/temp/AnimationFile_"+id+".txt";
        #endif
    }

    // Start is called before the first frame update
    void Start()
    {
        #if UNITY_WEBGL && !UNITY_EDITOR
        StartCoroutine(OutputRoutineOpen(url));
        #endif

        #if UNITY_EDITOR
        url = "http://127.0.0.1:5000/static/temp/AnimationFile.txt";
        StartCoroutine(OutputRoutineOpen(url));
        #endif
        slider = GameObject.Find("LectureBar").GetComponent<Slider>();

    }

    
    private IEnumerator OutputRoutineOpen(string url)
    {
        UnityWebRequest www = UnityWebRequest.Get(url);


        yield return www.SendWebRequest();
        
        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log("WWW ERROR: " + www.error);
        }
        else
        {
            byte[] bytes = www.downloadHandler.data;
            string s = new UTF8Encoding().GetString(bytes);
            lines = s.Split(new[] { "\r\n", "\r", "\n" }, StringSplitOptions.None).ToList();
            slider.maxValue = lines.Count-2;
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (lines.Count>0){
            isPlaying = GameObject.Find("PlayPause").GetComponent<PlayPauseButton>().isPlaying;
            if (isPlaying && slider.value<lines.Count-1){
                string[] points = lines[(int)slider.value].Split(',');   
                for (int i=0; i<=32;i++){
                    float x = float.Parse(points[0+i*3],CultureInfo.InvariantCulture)*10;
                    float y = float.Parse(points[1+i*3],CultureInfo.InvariantCulture)*10;
                    float z = float.Parse(points[2+i*3],CultureInfo.InvariantCulture)*3;
                    Body[i].transform.localPosition = new Vector3(x,y,z);
                }
                slider.value += 1 ;
            } else if (slider.value == lines.Count-2) { 
                if (tempPlayPauseStatus != isPlaying ){
                    slider.value = 0;
                }
            } else {
                if (slider.value != tempSliderValue){
                    string[] points = lines[(int)slider.value].Split(',');   
                    for (int i=0; i<=32;i++){
                        float x = float.Parse(points[0+i*3],CultureInfo.InvariantCulture)*10;
                        float y = float.Parse(points[1+i*3],CultureInfo.InvariantCulture)*10;
                        float z = float.Parse(points[2+i*3],CultureInfo.InvariantCulture)*3;
                        Body[i].transform.localPosition = new Vector3(x,y,z);
                    }
                }
            }
            
            tempSliderValue = slider.value;
            tempPlayPauseStatus = isPlaying;
        }
    }
}
