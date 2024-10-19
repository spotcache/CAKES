package com.example.cakes.controller;

import com.example.cakes.model.User;
import com.example.cakes.model.FileUpload;
import com.example.cakes.service.FileUploadService;
import com.example.cakes.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.security.Principal;

@Controller
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private FileUploadService fileUploadService;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    // ** Registration Page **
    @GetMapping("/register")
    public String showRegistrationForm(Model model) {
        model.addAttribute("user", new User());
        return "register"; // The HTML template in 'templates/register.html'
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
        return "login"; // The HTML template in 'templates/login.html'
    }

    // ** Upload File Page (Accessible only after login) **
    @GetMapping("/upload")
    public String showUploadForm(Model model) {
        model.addAttribute("fileUpload", new FileUpload());
        return "upload"; // The HTML template in 'templates/upload.html'
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

        // Find the user by username (from logged-in session)
        User user = userService.findByUsername(principal.getName());

        // Upload the file and store metadata in the database
        fileUploadService.uploadFile(file, duration, user);
        model.addAttribute("message", "File uploaded successfully!");
        return "upload";
    }
}
