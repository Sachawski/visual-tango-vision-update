using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class member_follow_line : MonoBehaviour
{
    public LineRenderer lineRenderer;
    public Transform cylinder;

    public Vector3 additionalRotationAxis = Vector3.up; // L'axe autour duquel vous voulez ajouter la rotation

    void Update()
    {
        // Mettez à jour la position du cylindre pour qu'il suive le Line Renderer
        Vector3 newPosition = (lineRenderer.GetPosition(1)+lineRenderer.GetPosition(0))/2; // Obtenez la position de la fin du Line Renderer
        cylinder.position = newPosition;

        // Faites en sorte que le cylindre regarde vers le point suivant du Line Renderer
        if (lineRenderer.positionCount > 1)
        {
            Vector3 nextPosition = lineRenderer.GetPosition(1);
            cylinder.LookAt(nextPosition,Vector3.right);
            // Calculez la rotation autour de l'axe X (ou Y, ou Z) que vous souhaitez appliquer au cylindre
            float rotationAngleX = 90f; // Exemple : rotation de 45 degrés autour de l'axe X

            // Appliquez la rotation au cylindre
            cylinder.Rotate(rotationAngleX, 0f, 0f, Space.Self);
        }
    }
}   