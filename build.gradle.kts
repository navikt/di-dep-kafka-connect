val vault_libs = configurations.create("vault_libs")
val jdbc_libs = configurations.create("jdbc_libs")

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
    jdbc_libs("com.oracle.database.jdbc:ojdbc8:12.2.0.1")
    jdbc_libs("com.datamountaineer:kafka-connect-common:1.1.9")
    jdbc_libs("com.github.navikt:complex-types-oracle-dialect:1.20200615105046.8df7cc9")
    vault_libs("com.bettercloud:vault-java-driver:5.1.0")
    vault_libs("com.github.navikt:kafka-connect-vault-provider:1.20200626073142.dbad512")
}

tasks.register<Copy>("buildJdbcLibs") {
    description = "Copy the JDBC libs to build directory"

    from(jdbc_libs)
    into("$buildDir/jdbc")
}

tasks.register<Copy>("buildVaultLibs") {
    description = "Copy the Vault libs to build directory"

    from(vault_libs)
    into("$buildDir/vault")
}

tasks.register("build") {
    dependsOn("buildVaultLibs", "buildJdbcLibs")
}
