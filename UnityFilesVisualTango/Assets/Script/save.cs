﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

// a class which keeps all the information for each step
public class Pose
{
    public int d = 0; // facedirection
    public int w = 0; // weighted leg
    public int p = 0; // pose 
    public int h = 0; // position of the weighted leg (height)
    public int t = 2; // slider (execution speed)
    public int r = 0; // body rotation
    public int lean = 0; // body leaning

    public void init(int dd = 0, int ww = 0, int pp = 0, int hh = 0, int tt = 0, int rr = 0, int ll = 0)
    {
        d = dd;
        w = ww;
        p = pp;
        h = hh;
        t = tt;
        r = rr;
        lean = ll;
    }
}

// a list that keeps all the poses
public static class streaming
{
    public static List<Pose> l = new List<Pose>();
    public static List<Pose> list
    {
        get
        {
            return l;
        }
        set
        {
            streaming.l = value;
        }
    }
}

// keep the number of the poses
public static class total
{
    public static int t = 0;
    public static int tot
    {
        get
        {
            return t;
        }
        set
        {
            total.t = value;
        }
    }
}

// tell which pose is selected by clicking on the logs in the right part of the screen (to delete and insert)
public static class selected
{
    public static int s = 0;
    public static int select
    {
        get
        {
            return s;
        }
        set
        {
            selected.s = value;
        }
    }
}

// what happens when "save" is clicked
// button is going to change its name
public class save : MonoBehaviour
{
    string[] Name = { "Collected", "Corssed forward", "Forward", "Backward", "In air forward", "In air backward", "Slide outside", "Wrapped around", "Collected high", "Crossed backward" };
    string[] Height = { "straight", "bent", "tiptoe" };
    string[] Leg = { "right", "left" };
    string[] Direction = { "north", "northwest", "northeast" };
    int[] angle = { 0, 30, 60, 90, 120, 150, 180, 270, 360 };
    string[] Leaning = {"straight","forward","backward"};
    // Start is called before the first frame update
    public GameObject PosListContent;
    public GameObject ButtonTemplate;
    public play playScript;
 
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
        button.onClick.AddListener(OnClick);
    }

    void OnClick()
    {
        int d = GameObject.Find("Facedir").GetComponent<Dropdown>().value;
        int w = GameObject.Find("Weighted").GetComponent<Dropdown>().value;
        int p = GameObject.Find("Pose").GetComponent<Dropdown>().value;
        int h = GameObject.Find("Position").GetComponent<Dropdown>().value;
        int r = angle[GameObject.Find("Rotate").GetComponent<Dropdown>().value];
        int t = (int)GameObject.Find("Slider").GetComponent<Slider>().value;
        int lean = GameObject.Find("Leaning").GetComponent<Dropdown>().value;

        Toggle rotate_dir = GameObject.Find("rotate_dir").GetComponent<Toggle>();
        if (!rotate_dir.isOn)
            r = -r;

        Pose tmp = new Pose();
        // save the pose
        tmp.init(d, w, p, h, t, r,lean);
        List<Pose> tmplist = new List<Pose>();
        // for insertion we need to have a new list for the poses
        for (int i = 0; i < selected.select; ++i)
        {
            tmplist.Add(streaming.l[i]);
        }
        tmplist.Add(tmp);
        for (int i = selected.select; i < total.tot; ++i)
        {
            tmplist.Add(streaming.l[i]);
        }
        streaming.list = tmplist;
        total.tot += 1;
        // after the insertion, cancel the clicked status and select the empty space after the last pose
        selected.select = total.tot;
        List<Pose> l = streaming.l;
        GameObject canvas = GameObject.Find("Canvas");
        // destroy all the old logs
        foreach (GameObject bs in GameObject.FindGameObjectsWithTag("log"))
        {
            Destroy(bs);
        }
        // create new logs
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
