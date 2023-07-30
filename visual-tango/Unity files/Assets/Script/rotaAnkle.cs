using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class rotaAnkle : MonoBehaviour
{

    private Animator mAnimator;
    int weightedLeg = 0;
    int rot_ank = 0;

    // Start is called before the first frame update
    void Start()
    {
        mAnimator = GetComponent<Animator>();
        int weightedLeg = GameObject.Find("Weighted").GetComponent<Dropdown>().value;
        GameObject.Find("RotateAnkle").GetComponent<Dropdown>().onValueChanged.AddListener(rotankle); 
    }

    // Update is called once per frame
    void Update()
    {
        if(mAnimator != null)
        {
            if (weightedLeg == 0){
                switch(rot_ank)
                {
                    case 1:
                        mAnimator.SetTrigger("Right");
                        break;
                    case 2:
                        mAnimator.SetTrigger("Left");
                        break;
                    default:
                        break;
                }
                
            }
        }
    }

    public void rotankle(int value){
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
}
