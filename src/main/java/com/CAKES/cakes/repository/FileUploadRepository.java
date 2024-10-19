package com.example.cakes.repository;

import com.example.cakes.model.FileUpload;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface FileUploadRepository extends JpaRepository<FileUpload, Long> {
    List<FileUpload> findByUser_Id(Long userId);
}
