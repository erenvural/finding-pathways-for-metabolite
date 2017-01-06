//package com.bio.project;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.net.URLDecoder;

public class GetPrecursors {

	public static String cursor;
	public static String mainCompound;
	public static String newSequence;
	public static Set<String> targetCompunds = new TreeSet<String>();
	public static Object[] targetArray;
	public static String[] filterList = { "H2O", "CO2", "ATP", "UTP" };

	public static void main(String[] args) throws IOException {

		// cursor = "glutamate";
		cursor = args[0].toString();
		String path = "output/" + cursor + ".clean.txt";
		String decodedPath = URLDecoder.decode(path);
		List<String> lines = Files.readAllLines(Paths.get(decodedPath));
		for (String line : lines) {
			if (line.contains(";")) {
				mainCompound = (String) line.substring(0, line.lastIndexOf(";"));
				newSequence = (String) line.substring(line.lastIndexOf(";") + 2, line.length());
			} else {
				mainCompound = "Unknown";
				newSequence = line;
			}
			String[] words = newSequence.split(" \\+ ");
			for (int i = 0; i < words.length; i++) {
				words[i] = words[i].trim();
				for (String filterTerm: filterList) {
					if (!words[i].contains(filterTerm)) {
						targetCompunds.add(words[i]);
					}	
				}
				
			}
		}
		path = "output/" + cursor + ".precursors.txt";
		decodedPath = URLDecoder.decode(path);
		File newFile = new File(decodedPath);
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
