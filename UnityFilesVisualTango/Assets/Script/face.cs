using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

// what happens when you change your selections of the dropdowns
// do not walk around and rotate

public class face : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        GameObject.Find("Facedir").GetComponent<Dropdown>().onValueChanged.AddListener(facedir);
        GameObject.Find("Weighted").GetComponent<Dropdown>().onValueChanged.AddListener(weight);
        GameObject.Find("Pose").GetComponent<Dropdown>().onValueChanged.AddListener(pose);
        GameObject.Find("Position").GetComponent<Dropdown>().onValueChanged.AddListener(position);
        GameObject.Find("Rotate").GetComponent<Dropdown>().onValueChanged.AddListener(rotate);
        GameObject.Find("Leaning").GetComponent<Dropdown>().onValueChanged.AddListener(lean);
        //GameObject.Find("RotateAnkle").GetComponent<Dropdown>().onValueChanged.AddListener(rotankle);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    int dir = 0;
    int wei = 0;
    int hei = 0;
    int pos = 0;
    //int rot = 0;
    int pre_wei = 0;
    private Toggle rotate_dir;

    // weighted leg pose
    public void show()
    {
        GameObject woman = GameObject.Find("Spine");
        Animator anis = woman.GetComponent<Animator>();
        anis.SetInteger("face", dir);

        GameObject leg_l = GameObject.Find("LeftUpLeg");
        Animator ani = leg_l.GetComponent<Animator>();
        GameObject leg_r = GameObject.Find("RightUpLeg");
        Animator ani0 = leg_r.GetComponent<Animator>();
        if (wei == 0) // right leg weighted
        {
            ani0.SetInteger("state", 0);
            if (hei == 1) // bent
            {
                ani0.SetInteger("hi", 1);
                ani.SetInteger("hi", 1);
            }
            else if (hei == 3) // tiptoe
            {
                ani0.SetInteger("hi", 2);
                ani.SetInteger("hi", 0);
            }
            else // straight
            {
                ani0.SetInteger("hi", 0);
                ani.SetInteger("hi", 0);
            }
            ani.SetInteger("state", pos);
        }
        else
        {
            ani.SetInteger("state", 0);
            if (hei == 1)
            {
                ani0.SetInteger("hi", 1);
                ani.SetInteger("hi", 1);
            }
            else if (hei == 3)
            {
                ani0.SetInteger("hi", 0);
                ani.SetInteger("hi", 2);
            }
            else
            {
                ani0.SetInteger("hi", 0);
                ani.SetInteger("hi", 0);
            }        
            ani0.SetInteger("state", pos);
            
        }
        stepAround();
    }

    
    void rotate(int value)
    {
        int rota_dir = 1;
        rotate_dir = GameObject.Find("rotate_dir").GetComponent<Toggle>();
        if (!rotate_dir.isOn)
            rota_dir = -rota_dir;

        switch(value){
            case 0:
                isTurning.r = rota_dir*0;
                break;
            case 1:
                isTurning.r = rota_dir*30;
                break;    
            case 2:
                isTurning.r = rota_dir*60;
                break;
            case 3:
                isTurning.r = rota_dir*90;
                break;
            case 4:
                isTurning.r = rota_dir*120;
                break;
            case 5:
                isTurning.r = rota_dir*150;
                break;
            case 6:
                isTurning.r = rota_dir*180;
                break;    
            case 7:
                isTurning.r = rota_dir*270;
                break;
            case 8:
                isTurning.r = rota_dir*360;
                break;
        }
        show();
    }

    // calculate how far the women moves totally
    // "isMoving" class is defined in around.cs
    void stepAround()
    {
        GameObject model = GameObject.Find("dance");
        GameObject leg_r = GameObject.Find("RightUpLeg");
        GameObject leg_rr = GameObject.Find("RightLeg");
        GameObject leg_l = GameObject.Find("LeftUpLeg");
        GameObject leg_ll = GameObject.Find("LeftLeg");
        if (pre_wei == 0) // in the former pose, she weighted on the right leg
        {
            if (wei == 1)// change the weight to the left leg, so move to where the left feet is
            {
                isMoving.m = 1;
                isMoving.tmp = model.transform.position;
                isMoving.xx = (float)(Mathf.Sin(leg_l.transform.rotation.x) * 1.50 + Mathf.Sin(leg_ll.transform.rotation.x) * 0.7);
                isMoving.zz = (float)(-Mathf.Sin(leg_l.transform.rotation.z) * 1.50 - Mathf.Sin(leg_ll.transform.rotation.z) * 0.7);
            }
            else
                return;
        }
        else // in the former pose, she weighted on the left leg
        {
            if (wei == 0) // change the weight to the right leg
            {
                isMoving.m = 1;
                isMoving.tmp = model.transform.position;
                isMoving.xx = (float)(Mathf.Sin(leg_r.transform.rotation.x) * 1.50 + Mathf.Sin(leg_rr.transform.rotation.x) * 0.7);
                isMoving.zz = (float)(-Mathf.Sin(leg_r.transform.rotation.z) * 1.50 - Mathf.Sin(leg_rr.transform.rotation.z) * 0.7);
                //model.transform.position = tmp + new Vector3((float)(-Mathf.Sin(leg_r.transform.rotation.x) * 0.95 - Mathf.Sin(leg_rr.transform.rotation.x) * 0.5), 0, (float)(-Mathf.Sin(leg_r.transform.rotation.z) * 0.95 - Mathf.Sin(leg_rr.transform.rotation.z) * 0.5));
            }
            else
                return;
        }
        pre_wei = wei;
    }


    /*
    public void rotankle(int value){
        {
            switch(value)
            {
                case 0:
                    rot_ank = 0;
                    break;
                case 1:
                    rot_ank = 1;
                    break;
                case 2:
                    rot_ank = 2;
                    break;
                case 3:
                    rot_ank = 3;
                    break;
            }
        }
        show();
    }
    */

    // changing free leg pose
    public void pose(int value)
    {
        print(value);
        switch (value)
        {
            case 0:
                pos = 2;
                break;
            case 1:
                pos = 3;
                break;
            case 2:
                pos = 1;
                break;
            case 3:
                pos = 4;
                break;
            case 4:
                pos = 5;
                break;
            case 5:
                pos = 6;
                break;
            case 6:
                pos = 7;
                break;
            case 7:
                pos = 8;
                break;
            case 8:
                pos = 9;
                break;
            case 9:
                pos = 10;
                break;
        }

        show();
    }

    // changing the height
    public void position(int value)
    {
        GameObject model = GameObject.Find("dance");
        Animator ani = model.GetComponent<Animator>();
        GameObject leg_l = GameObject.Find("LeftUpLeg");
        Animator ani1 = leg_l.GetComponent<Animator>();
        GameObject leg_r = GameObject.Find("RightUpLeg");
        Animator ani0 = leg_r.GetComponent<Animator>();
        switch (value)
        {
            case 0:
                //if (hei == 1)
                ani.SetInteger("state", 2);
                hei = 0;
                ani0.SetInteger("hi", 0);
                ani1.SetInteger("hi", 0);
                break;
            case 1:
                ani.SetInteger("state", 1);
                hei = 1;
                ani0.SetInteger("hi", 1);
                ani1.SetInteger("hi", 1);
                break;
            case 2:
                ani.SetInteger("state", 3);
                hei = 3;
                ani0.SetInteger("hi", 2);
                ani1.SetInteger("hi", 2);
                break;
        }
        show();
    }

    // changing the weighted leg
    public void weight(int value)
    {
        wei = value;
        show();
    }


    // changing the face direction
    public void facedir(int value)
    {
        GameObject woman = GameObject.Find("Spine");
        Animator ani = woman.GetComponent<Animator>();
       
        switch (value)
        {
            case 0:
                //if (dir == 1)
                //    ani.SetInteger("face", 4);
                //else if (dir == 2)
                //    ani.SetInteger("face", 2);
                dir = 0;
                break;
            case 1:
                //if (dir == 0)
                //    ani.SetInteger("face", 3);
                dir = 1;
                break;
            case 2:
                //if (dir == 0)
                //    ani.SetInteger("face", 1);
                dir = 2;
                break;
        }
        show();
    }

    public void lean(int value)
    {
        GameObject hips = GameObject.Find("Hips");
        Animator ani_hips = hips.GetComponent<Animator>();
        switch (value)
        {
            case 0:
                if (ani_hips.isActiveAndEnabled){
                    ani_hips.SetInteger("lean",0);
                }
                break;
            case 1:
                if (ani_hips.isActiveAndEnabled){
                    ani_hips.SetInteger("lean",1);
                }
                break;
            case 2:
                if (ani_hips.isActiveAndEnabled){
                    ani_hips.SetInteger("lean",2);
                }
                break;
        }
        show();
    }
}
