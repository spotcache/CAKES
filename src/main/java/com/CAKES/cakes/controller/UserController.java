package com.example.cakes.controller;

import com.example.cakes.model.User;
import com.example.cakes.model.FileUpload;
import com.example.cakes.service.FileUploadService;
import com.example.cakes.service.UserService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.security.Principal;

@Controller
public class UserController {

    private final UserService userService;
    private final FileUploadService fileUploadService;
    private final BCryptPasswordEncoder passwordEncoder;

    public UserController(UserService userService, FileUploadService fileUploadService, BCryptPasswordEncoder passwordEncoder) {
        this.userService = userService;
        this.fileUploadService = fileUploadService;
        this.passwordEncoder = passwordEncoder;
    }

    // ** Registration Page **
    @GetMapping("/register")
    public String showRegistrationForm(Model model) {
        model.addAttribute("user", new User());
        return "register";
    }

    @PostMapping("/register")
    public String registerUser(@ModelAttribute("user") User user, Model model) {
        if (userService.findByUsername(user.getUsername()) != null) {
            model.addAttribute("error", "Username already taken");
            return "register";
        }
        // Encrypt password before saving
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        userService.saveUser(user);
        return "redirect:/login";
    }

    // ** Login Page **
    @GetMapping("/login")
    public String showLoginForm() {
        return "login";
    }

    // ** Upload File Page (Accessible only after login) **
    @GetMapping("/upload")
    public String showUploadForm(Model model) {
        model.addAttribute("fileUpload", new FileUpload());
        return "upload";
    }

    @PostMapping("/upload")
    public String handleFileUpload(@RequestParam("file") MultipartFile file, 
                                   @RequestParam("duration") int duration, 
                                   Principal principal, 
                                   Model model) {
        if (file.isEmpty()) {
            model.addAttribute("error", "No file selected");
            return "upload";
        }

        // Upload the file and store metadata in the database
        fileUploadService.uploadFile(file, duration, userService.findByUsername(principal.getName()));
        model.addAttribute("message", "File uploaded successfully!");
        return "upload";
    }
}
