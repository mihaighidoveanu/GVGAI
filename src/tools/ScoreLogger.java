package tools;

import java.util.stream.Collectors;
import java.util.stream.Stream;

import java.io.PrintWriter;
import java.io.File;
import java.io.IOException;

import java.util.List;
import java.util.ArrayList;

public class ScoreLogger {

    private File outputFile;
    private String outputName;
    private List<String[]> dataLines = new ArrayList<>();

    public ScoreLogger(String outputName){
        this.outputName = outputName;
        this.dataLines.add(new String[]{"game,win,score,time"});
    }
    
    public String escapeSpecialCharacters(String data) {
        String escapedData = data.replaceAll("\\R", " ");
        if (data.contains(",") || data.contains("\"") || data.contains("'")) {
            data = data.replace("\"", "\"\"");
            escapedData = "\"" + data + "\"";
        }
        return escapedData;
    }

    public String convertToCSV(String[] data) {
        return Stream.of(data)
            .map(this::escapeSpecialCharacters)
            .collect(Collectors.joining(","));
    }

    public void write() throws IOException {
        System.out.println("Writing logs in " + this.outputName);
        if (this.outputFile == null) {
            this.outputFile = new File(this.outputName);
        }
        try (PrintWriter pw = new PrintWriter(this.outputFile)) {
            dataLines.stream()
              .map(this::convertToCSV)
              .forEach(pw::println);
        }
        // assertTrue(this.outputFile.exists());
        assert this.outputFile.exists();
    }

    public void log(String gameFile, double victory, double score, int timestamp){
        this.dataLines.add(new String[]{
            gameFile, String.valueOf(victory), String.valueOf(score), String.valueOf(timestamp)
        });

	    System.out.println("Logging in game " + gameFile + ", " + victory + " , " + score + " , " + timestamp);

    }
}
