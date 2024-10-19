package com.example.cakes.model;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
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
}
