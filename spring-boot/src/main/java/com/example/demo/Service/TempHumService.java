package com.example.demo.Service;

import com.example.demo.Model.TempHumEntity;
import com.example.demo.repository.TempHumRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class TempHumService {
    
    @Autowired
    private TempHumRepository tempHumRepository;
    
    public Optional<TempHumEntity> getLatestReading() {
        return tempHumRepository.findTopByOrderByTimestampDesc();
    }
    
    public TempHumEntity getLatestReadingOrDefault() {
        return tempHumRepository.findTopByOrderByTimestampDesc()
                .orElse(new TempHumEntity("0", 0.0, 0, null));
    }

    public Optional<TempHumEntity> getLatestReadingById() {
        return tempHumRepository.findTopByOrderByIdDesc();
    }
}