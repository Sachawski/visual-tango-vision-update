using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayPauseButton : MonoBehaviour
{
    private Button playPauseButton;
    public bool isPlaying = false;

    private void Start()
    {
        playPauseButton = GetComponent<Button>();
        playPauseButton.onClick.AddListener(ToggleAnimation);
    }

    private void ToggleAnimation()
    {
        isPlaying = !isPlaying;
    }
}
