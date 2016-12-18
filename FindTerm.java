//package com.bio.project;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class FindTerm {
	
	
	public static int totalSequenceNumber = 1, targetCompoundNumber = 0;
	public static ArrayList<String> allTerms = new ArrayList<String>();
	public static ArrayList<String> targetCompunds = new ArrayList<String>();
	
	public static void main(String[] args) throws IOException {
		/*File dir=new File("");
		File[] list=dir.listFiles();
		for(int i=0;i<list.length;i++){
		     allTerms.add(list[i].getName());
		    }  
		*/

	    String search_key = args[0].toString();
		List<String> filecontents = Files.readAllLines(Paths.get(search_key + ".txt"));
		for (String line: filecontents) {
			// System.out.println(line);
			String mainCompound = (String) line.substring(0, line.indexOf(";"));
			System.out.println("√ Valid Sequence ! Main Compound = " + mainCompound);
		}
		//System.out.println(filecontents.size());
		
		/*
		for (String cursor : allTerms) {
			cursor = cursor.replace(".txt", "");
			List<String> lines = Files.readAllLines(Paths.get(cursor+".txt"));
			for (String line : lines) {
				if (line.indexOf(cursor) < line.indexOf(">")) {
					System.out.println("X Invalid Sequence  ");
				} else {
					if (line.contains(";")) {
						String mainCompound = (String) line.substring(0, line.indexOf(";"));
						System.out.println("√ Valid Sequence ! Main Compound = " + mainCompound);
						String newSequence = (String) line.substring(line.indexOf(";") + 2, line.length());
						System.out.println("Full sequence = " + newSequence);
						System.out.println();
						String[] sides = newSequence.split("<=>");
						String leftSide = sides[0];
						String rightSide = sides[1];
						System.out.print("Left Side = " + leftSide);
						rightSide = rightSide.trim();
						System.out.println("  |  Right Side = " + rightSide);
						System.out.println();
						System.out.println("All Compounds in Left Side");
						String[] words = leftSide.split(" \\+ ");
						ArrayList<String> usefulCompounds = new ArrayList<String>();
						ArrayList<String> uselessCompounds = new ArrayList<String>();
						for (int i = 0; i < words.length; i++) {
							words[i] = words[i].trim();
							if (words[i] != " ") {
								System.out.println(i + 1 + ". " + words[i]);
							}

							if (targetCompunds.contains(words[i])) {
								
							}
							else {
								targetCompunds.add(words[i]);
								targetCompoundNumber++;
							}
//							if (words[i].contains("H2O") || words[i].contains("CO2") || words[i].contains("ATP")
//									|| words[i].contains("ADP") || words[i].contains("H")) {
//								uselessCompounds.add(words[i]);
//							} else {
//								usefulCompounds.add(words[i]);
//								if (targetCompunds.contains(words[i])) {
	//
//								} else {
//									targetCompunds.add(words[i]);
//									targetCompoundNumber++;
//								}
							}
						System.out.println("----------------------------------------------------------------------------------");
						}
//						System.out.println();
//						System.out.println("Useless Compounds; ");
//						for (String compound : uselessCompounds) {
//							System.out.println(compound);
//						}
//						System.out.println();
//						System.out.println("Useful Compounds; ");
//						for (String compound : usefulCompounds) {
//							System.out.println(compound);
//						}
//						System.out.println("----------------------------------------------------------------------------------");
//					} else {
						System.out.print(totalSequenceNumber / 2 + 1 + "-> ");
//					}
				}
				totalSequenceNumber++;
			}

			File newFile = new File("C:\\Users\\eren\\Desktop\\File\\" + cursor + "Precusors.txt");
			FileWriter myWriter = new FileWriter(newFile);
			BufferedWriter iWrite = new BufferedWriter(myWriter);
			System.out.println("______________ FINAL RESULTS __________________");
			System.out.println(cursor + "'s target compounds are below in "+totalSequenceNumber/2+" total sequence." );
			for (int i = 0; i < targetCompunds.size(); i++) {
				System.out.println("• " + targetCompunds.get(i));
				iWrite.write(targetCompunds.get(i).toString() + "\n");
			}
			iWrite.close();
			System.out.println();
			System.out.println(targetCompoundNumber + " Target Compounds");
			System.out.println("________________________________________________");
			
		}
	*/
	}
}
