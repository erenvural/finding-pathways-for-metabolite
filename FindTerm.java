package com.bio.project;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;	

public class FindTerm {

	public static String cursor;
	public static int totalSequenceNumber = 0, targetCompoundNumber = 0;
	public static String mainCompound;
	public static String newSequence;
	public static ArrayList<String> targetCompunds = new ArrayList<String>();

	public static void main(String[] args) throws IOException {

		cursor = "glutamate";
		//cursor = args[0].toString();
		List<String> lines = Files.readAllLines(Paths.get("C:\\Users\\eren\\Desktop\\File\\" + cursor + ".txt"));
		for (String line : lines) {
			System.out.print(totalSequenceNumber+1 + "-> ");
			if (line.contains(";")) {
				mainCompound = (String) line.substring(0, line.indexOf(";"));
				newSequence = (String) line.substring(line.indexOf(";") + 2, line.length());
			}
			else {
				mainCompound = "Unknown";
				newSequence = line;
			}
			System.out.println("Main Compound = " + mainCompound);
			System.out.println("Full sequence = " + newSequence);
			System.out.println();
			System.out.println("All Compounds");
			String[] words = newSequence.split(" \\+ ");
			for (int i = 0; i < words.length; i++) {
				words[i] = words[i].trim();
				if (words[i] != " ") {
					System.out.println(i + 1 + ". " + words[i]);
				}

				if (targetCompunds.contains(words[i])) {

				} else {
					targetCompunds.add(words[i]);
					targetCompoundNumber++;
				}
			}
			System.out.println("----------------------------------------------------------------------------------");
			totalSequenceNumber++;
		}

		File newFile = new File("C:\\Users\\eren\\Desktop\\File\\" + cursor + "Precusors.txt");
		FileWriter myWriter = new FileWriter(newFile);
		BufferedWriter iWrite = new BufferedWriter(myWriter);
		System.out.println("______________ FINAL RESULTS __________________");
		System.out.println(cursor + "'s target compounds are below in " + totalSequenceNumber + " total sequence.");
		for (int i = 0; i < targetCompunds.size(); i++) {
			System.out.println(i+1 +") • " + targetCompunds.get(i));
			iWrite.write(targetCompunds.get(i).toString() + "\n");
			
		}
		iWrite.close();
		System.out.println();
		System.out.println(targetCompoundNumber + " Target Compounds");
		System.out.println("________________________________________________");
	}
}
