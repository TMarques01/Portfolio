package com.example.demo.repository;

import com.example.demo.Model.TempHumEntity;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import java.util.Optional;

// This interface extends MongoRepository, which provides CRUD operations for TempHumEntity.
public interface TempHumRepository extends MongoRepository<TempHumEntity, String> {

    // Busca o último registro ordenado por timestamp decrescente
    Optional<TempHumEntity> findTopByOrderByTimestampDesc();

    Optional<TempHumEntity> findTopByOrderByIdDesc();

    // @Query(value = "{}", sort = "{ 'timestamp': -1 }")
    // Optional<TempHumEntity> findLatestByTimestamp();
    
}