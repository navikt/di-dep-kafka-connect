
val libs = configurations.create("libs")

val githubUser: String? by project
val githubPassword: String? by project

repositories {
    mavenCentral()
    jcenter()

    maven {
        name = "complex-types-oracle-jdbc-dialect"
        url = uri("https://maven.pkg.github.com/navikt/complex-types-oracle-jdbc-dialect")
        credentials {
            username = githubUser ?: "x-access-token"
            password = githubPassword ?: System.getenv("GITHUB_TOKEN")
        }
    }

    maven {
        name = "kafka-connect-vault-provider"
        url = uri("https://maven.pkg.github.com/navikt/kafka-connect-vault-provider")
        credentials {
            username = githubUser ?: "x-access-token"
            password = githubPassword ?: System.getenv("GITHUB_TOKEN")
        }
    }
}

configurations.all {
    isTransitive = false
}

dependencies {
    libs("com.oracle.database.jdbc:ojdbc8:12.2.0.1")
    libs("com.datamountaineer:kafka-connect-common:1.1.9")
    libs("com.bettercloud:vault-java-driver:5.1.0")
    libs("com.github.navikt:complex-types-oracle-dialect:1.20200615105046.8df7cc9")
    libs("com.github.navikt:kafka-connect-vault-provider:1.20200615135031.6f8122f")
}

tasks.register<Copy>("build") {
    description = "Copy the libs to build directory"

    from(libs)
    into("$buildDir")
}
