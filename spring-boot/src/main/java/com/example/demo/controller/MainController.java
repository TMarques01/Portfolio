package com.example.demo.controller;

import com.example.demo.Model.TempHumEntity;
import com.example.demo.repository.TempHumRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import java.util.Optional;

@Controller
public class MainController {

    @Autowired
    private TempHumRepository tempHumRepository;

    @GetMapping("/")
    public String index() { return "index"; }

    @GetMapping("/information")
    public String information() { return "information"; }

    @GetMapping("/music")
    public String music() { return "music"; }

    @GetMapping("/music/personal")
    public String musicPersonal() { return "music_personal"; }

    @GetMapping("/music/lauslater")
    public String musicLauSlater() { return "music_lauslater"; }

    @GetMapping("/other")
    public String other(Model model) {
        System.out.println("=== ENTRANDO NO ENDPOINT /other ===");
        
        try {
            // Verificar se o repository está injetado
            if (tempHumRepository == null) {
                System.out.println("ERRO: Repository é null!");
                return "other";
            }
            
            // Buscar apenas o dado mais recente com o método 2
            Optional<TempHumEntity> result = tempHumRepository.findTopByOrderByTimestampDesc();
            
            if (result.isPresent()) {
                TempHumEntity latestReading = result.get();
                System.out.println("Dados encontrados: ID=" + latestReading.getId() + 
                      ", Temp=" + latestReading.getTemperature() + 
                      ", Hum=" + latestReading.getHumidity());
                model.addAttribute("latestReading", latestReading);
            } else {
                System.out.println("Nenhum dado encontrado! Criando dados padrão.");
                TempHumEntity defaultReading = new TempHumEntity("999", 25.5, 60, java.time.LocalDateTime.now());
                model.addAttribute("latestReading", defaultReading);
            }
            
        } catch (Exception e) {
            System.err.println("ERRO ao buscar dados: " + e.getMessage());
            TempHumEntity defaultReading = new TempHumEntity("999", 25.5, 60, java.time.LocalDateTime.now());
            model.addAttribute("latestReading", defaultReading);
        }
        
        return "other";
    }
}