package com.example.demo.Model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Document(collection = "TempHum")
public class TempHumEntity {

    @Id
    private int id;
    private double temperature;
    private double humidity;
    private LocalDateTime timestamp;

    public TempHumEntity() { }

    public TempHumEntity(double temperature, double humidity, LocalDateTime timestamp) {
        this.temperature = temperature;
        this.humidity = humidity;
        this.timestamp = timestamp;
    }
    
    public TempHumEntity(int id, double temperature, double humidity, LocalDateTime timestamp) {
        this.id = id;
        this.temperature = temperature;
        this.humidity = humidity;
        this.timestamp = timestamp;
    }
    
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public double getTemperature() {
        return temperature;
    }

    public void setTemperature(double temperature) {
        this.temperature = temperature;
    }

    public double getHumidity() {
        return humidity;
    }

    public void setHumidity(double humidity) {
        this.humidity = humidity;
    }

    public LocalDateTime getTimestamp() {
        return timestamp;
    }
}