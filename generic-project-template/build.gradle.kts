plugins {
    java
    jacoco
    id("org.springframework.boot") version "2.6.3" apply false
    id("io.spring.dependency-management") version "1.0.11.RELEASE" apply false
}

group = "com.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    // Logging
    implementation("org.slf4j:slf4j-api:1.7.32")
    implementation("org.slf4j:slf4j-simple:1.7.32")

    // JSON Processing
    implementation("com.fasterxml.jackson.core:jackson-databind:2.13.0")

    // Testing
    testImplementation("org.junit.jupiter:junit-jupiter-api:5.8.1")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.8.1")
    testImplementation("org.mockito:mockito-core:4.2.0")
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

tasks.test {
    useJUnitPlatform()
    finalizedBy(tasks.jacocoTestReport)
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(false)
        csv.required.set(false)
        html.outputLocation.set(layout.buildDirectory.dir("jacocoHtml"))
    }
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
}

// Configuration for different environments
configurations {
    create("developmentOnly")
    runtimeClasspath {
        extendsFrom(configurations["developmentOnly"])
    }
}

// Optional: Spring Boot configuration if needed
// apply(plugin = "org.springframework.boot")
// apply(plugin = "io.spring.dependency-management")
