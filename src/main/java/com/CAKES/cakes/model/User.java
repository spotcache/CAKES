package main.java.com.CAKES.cakes.model;

@Data
@Entity
public class User {

    private static final String GenerationType = null;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false, unique = false)
    private String password;
}
