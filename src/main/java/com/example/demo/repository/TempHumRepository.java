package com.example.demo.repository;

import com.example.demo.Model.TempHumEntity;
import org.springframework.data.mongodb.repository.MongoRepository;

// This interface extends MongoRepository, which provides CRUD operations for TempHumEntity.
public interface TempHumRepository extends MongoRepository<TempHumEntity, String> {}