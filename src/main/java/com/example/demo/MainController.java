package com.example.demo;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

@Controller
public class MainController {

    @GetMapping("/")
    public String index() {
        return "index";
    }
    @GetMapping("/information")
    public String information() {
        return "information";
    }


}