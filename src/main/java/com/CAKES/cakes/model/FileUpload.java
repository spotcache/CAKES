package com.example.cakes.model;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
public class FileUpload {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String filename;
    private LocalDateTime uploadTime;
    private LocalDateTime lastCheckin;

    private int timerDuration;  // in hours

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    // Getters and Setters
    // ...
}
