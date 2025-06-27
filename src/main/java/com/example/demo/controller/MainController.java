package com.example.demo.controller;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
public class MainController {

    @GetMapping("/")
    public String index() { return "index"; }

    @GetMapping("/information")
    public String information() { return "information"; }

    @GetMapping("/other")
    public String other() { return "other"; }
    
    @GetMapping("/music")
    public String music() { return "music"; }

    @GetMapping("/music/personal")
    public String musicPersonal() { return "music_personal"; }

    @GetMapping("/music/lauslater")
    public String musicLauSlater() { return "music_lauslater"; }

    @GetMapping("/music/other")
    public String musicOther() { return "music_otherprojects"; }
}