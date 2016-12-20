package com.bio.project;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public class FindTerm {

	public static String cursor;
	public static String mainCompound;
	public static String newSequence;
	public static Set<String> targetCompunds = new TreeSet<String>();
	public static Object[] targetArray;

	public static void main(String[] args) throws IOException {

		cursor = "glutamate";
		// cursor = args[0].toString();
		List<String> lines = Files.readAllLines(Paths.get("C:\\Users\\eren\\Desktop\\File\\" + cursor + ".clean.txt"));
		for (String line : lines) {
			if (line.contains(";")) {
				mainCompound = (String) line.substring(0, line.indexOf(";"));
				newSequence = (String) line.substring(line.indexOf(";") + 2, line.length());
			} else {
				mainCompound = "Unknown";
				newSequence = line;
			}
			String[] words = newSequence.split(" \\+ ");
			for (int i = 0; i < words.length; i++) {
				targetCompunds.add(words[i]);
			}
		}
		File newFile = new File("C:\\Users\\eren\\Desktop\\File\\" + cursor + ".precusors.txt");
		FileWriter myWriter = new FileWriter(newFile);
		BufferedWriter iWrite = new BufferedWriter(myWriter);
		// System.out.println("______________ FINAL RESULTS __________________");
		targetArray = targetCompunds.toArray();
		for (Object t : targetArray) {
			iWrite.write(t.toString() + "\n");
		}
		// iWrite.write(targetCompunds.size()+" target compounds !");
		iWrite.close();
	}
}
