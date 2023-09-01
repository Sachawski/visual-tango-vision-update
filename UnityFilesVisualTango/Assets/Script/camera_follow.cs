using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraFollow : MonoBehaviour
{

    public Transform target; // L'objet que la caméra doit suivre
    private Vector3 constante;

    void LateUpdate()
    {
        if (target != null)
        {
            // Calquer la position de la caméra sur la position de l'objet
            constante = new Vector3(0.0f,0.0f,-2.5f);
            transform.position = target.position + constante;

        }
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
