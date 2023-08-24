using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using System.IO;
using System.Text;
using UnityEngine.UI;
using SFB;
using System.Runtime.InteropServices; // Add this line
using UnityEngine.Networking;

public class load_file : MonoBehaviour
{
    #if UNITY_WEBGL && !UNITY_EDITOR
    [DllImport("__Internal")]
    private static extern string GetURLFromPage();
    [DllImport("__Internal")]
    private static extern string GetIDFromPage();
    #endif

    string[] Name = { "Collected", "Corssed forward", "Forward", "Backward", "In air forward", "In air backward", "Slide outside", "Wrapped around", "Collected high", "Crossed backward" };
    string[] Height = { "straight", "bent", "tiptoe" };
    string[] Leg = { "right", "left" };
    string[] Direction = { "north", "northwest", "northeast" };
    int[] angle = { 0, 30, 60, 90, 120, 150, 180, 270, 360 };
    string[] Leaning = {"straight","forward","backward"};
    private string url = "";
    private string id = "";
    public GameObject PosListContent;
    public GameObject ButtonTemplate;
    public play playScript;
  
  

    // Start is called before the first frame update
    void Start()
    {
        #if UNITY_WEBGL && !UNITY_EDITOR
        StartCoroutine(OutputRoutineOpen(url));
        #endif  
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void Awake()
    {
        Button button = gameObject.GetComponent<Button>() as Button;
        button.onClick.AddListener(Load);
        #if UNITY_WEBGL && !UNITY_EDITOR
        id = GetIDFromPage();
        url = GetURLFromPage() + "/static/temp/save_"+id+".txt";
        #endif
    }
    
    void Load()
    {
    	// Requesting a file from the user
        FileUploaderHelper.RequestFile((path) => 
        {
        		// If the path is empty, ignore it.
            if (string.IsNullOrWhiteSpace(path))
                return;
						
            // Run a coroutine to load an image
            StartCoroutine(OutputRoutineOpen(path));    
        });
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
        clear();
        for (int i = 0; i < s.Length; i += 8)
        {
            Pose p = new Pose();
            p.p = Int32.Parse(s[i].ToString());
            p.h = Int32.Parse(s[i + 1].ToString());
            p.w = Int32.Parse(s[i + 2].ToString());
            p.d = Int32.Parse(s[i + 3].ToString());
            p.t = Int32.Parse(s[i + 4].ToString());
            p.r = angle[Int32.Parse(s[i + 6].ToString())] - 2*Int32.Parse(s[i+5].ToString())*angle[Int32.Parse(s[i + 6].ToString())]  ;
            p.lean = Int32.Parse(s[i + 7].ToString());
            streaming.l.Add(p);
            total.tot += 1;
        }
        GameObject canvas = GameObject.Find("Canvas");
        List<Pose> l = streaming.l;
        Debug.Log("debutDestroy");
        foreach (GameObject bs in GameObject.FindGameObjectsWithTag("log"))
        {
            Destroy(bs);
        }
        Debug.Log("finDestroy");
        for (int i = 0; i < total.t; ++i)
        {
            int index = i;
            GameObject button = (GameObject)Instantiate(ButtonTemplate);
            button.transform.SetParent(PosListContent.transform);
            button.transform.localScale = new Vector3(3.5f,0.5f,1f);
            Button B = button.GetComponent<Button>();
            B.tag = "log";
            //B.GetComponent<RectTransform>().pivot = new Vector2(0, 0);
            

            GameObject temp = new GameObject("Text", typeof(RectTransform), typeof(Text));
            temp.transform.SetParent(button.transform);
            Text text = temp.GetComponent<Text>();
            text.tag = "text0";
            //text.GetComponent<RectTransform>().anchoredPosition = new Vector2(0, 0);
            //text.GetComponent<RectTransform>().sizeDelta = new Vector2(300, 20);
            text.GetComponent<Text>().horizontalOverflow = HorizontalWrapMode.Overflow;
            text.GetComponent<Text>().verticalOverflow = VerticalWrapMode.Overflow;
            //text.GetComponent<RectTransform>().pivot = new Vector2(0, 0);
            //text.GetComponent<RectTransform>().anchorMax = new Vector2(1, 1);
            //text.GetComponent<RectTransform>().anchorMin = new Vector2(0, 0);
            
            text.text = "";
            text.text += Name[l[i].p];
            text.text += ", ";
            text.text += Height[l[i].h];
            text.text += ", ";
            text.text += Leg[l[i].w];
            text.text += ", ";
            text.text += Direction[l[i].d];
            text.text += ", ";
            text.text += (l[i].t).ToString();
            text.text += ", ";
            text.text += (l[i].r).ToString();
            text.text += ", ";
            text.text += Leaning[l[i].lean];
            text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            text.fontSize = 15;
            text.alignment = TextAnchor.MiddleCenter;
            text.fontStyle = FontStyle.Normal;
            text.color = Color.black;
            //text.text += '\n';
            B.onClick.AddListener(delegate () {// if the log is clicked, the text would be bold and select this log
                selected.select = index;
                foreach (GameObject ts in GameObject.FindGameObjectsWithTag("text0"))
                {
                    ts.GetComponent<Text>().fontStyle = FontStyle.Normal;
                }
                text.fontStyle = FontStyle.BoldAndItalic;
                //Debug.Log(selected.select);
                playScript.go(index);
            });
            
        }

        }
    }

    void clear()
    {
        streaming.l = new List<Pose>();
        total.t = 0;
        selected.s = 0;
    }

}
