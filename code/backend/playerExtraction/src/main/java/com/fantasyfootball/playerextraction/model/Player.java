package com.fantasyfootball.playerextraction.model;

import org.springframework.data.annotation.Id;

import com.azure.spring.data.cosmos.core.mapping.Container;

@Container(containerName = "playerdata")
public class Player {

    @Id
    String id;
    String teams;
    String name;
    String position; 
    String points; 
    String worth;
    String jersey;

    public Player(String id, String teams, String name, String position, String points, String worth, String jersey) {
        this.id = id;
        this.teams = teams;
        this.name = name;
        this.position = position;
        this.points = points;
        this.worth = worth;
        this.jersey = jersey;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTeams() {
        return teams;
    }

    public void setTeams(String teams) {
        this.teams = teams;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPosition() {
        return position;
    }

    public void setPosition(String position) {
        this.position = position;
    }

    public String getPoints() {
        return points;
    }

    public void setPoints(String points) {
        this.points = points;
    }

    public String getWorth() {
        return worth;
    }

    public void setWorth(String worth) {
        this.worth = worth;
    }

    public String getJersey() {
        return jersey;
    }

    public void setJersey(String jersey) {
        this.jersey = jersey;
    }

    @Override
    public String toString() {
        return "Player [id=" + id + ", teams=" + teams + ", name=" + name + ", position=" + position + ", points="
                + points + ", worth=" + worth + ", jersey=" + jersey + "]";
    }   

}