package com.gen;

import java.io.*;
import java.util.Random;
import java.util.Scanner;

public class GenerateFile {

	public static void main(String[] args) throws IOException {
		String name_file = "";
		GenerateFile gf = new GenerateFile();

		String name_folder;
		Scanner scanner = new Scanner(System.in);
		System.out
				.println("Select the size you want :\n 1KB \n\n 10KB\n\n 100KB \n\n 1MB \n\n 10MB \n\n 100MB \n\n");
		name_folder = scanner.nextLine();
		System.out.println("The size you have choosen is " + name_folder);

		if(name_folder.equals("1KB")){
			for (int k = 0; k < 100; k++) {

				new File("./" + name_folder).mkdirs();
				name_file = "1KB/" + gf.random_string_create(10) + ".txt";

				File file = new File(name_file);

				FileWriter filewrite = new FileWriter(file);
				BufferedWriter bufferwriter = new BufferedWriter(filewrite);
				int i;
				for (i = 0; i < 10; i++) {
					bufferwriter.write(gf.random_string_create(99));
					bufferwriter.write("\n");
				}
				bufferwriter.write(gf.random_string_create(24));
				bufferwriter.close();
			}}
		    else if(name_folder.equals("10KB")){
			for (int k = 0; k < 100; k++) {
				new File("./" + name_folder).mkdirs();
				name_file = "10KB/" + gf.random_string_create(10) + ".txt";

				File file = new File(name_file);

				FileWriter filewrite = new FileWriter(file);
				BufferedWriter bufferwriter = new BufferedWriter(filewrite);
				int i;
				for (i = 0; i < 10; i++) {
					bufferwriter.write(gf.random_string_create(999));
					bufferwriter.write("\n");
				}
				bufferwriter.write(gf.random_string_create(240));
				bufferwriter.close();
			}}
		    else if(name_folder.equals("100KB")){
			for (int k = 0; k < 100; k++) {
				new File("./" + name_folder).mkdirs();
				name_file = "100KB/" + gf.random_string_create(10) + ".txt";

				File file = new File(name_file);

				FileWriter filewrite = new FileWriter(file);
				BufferedWriter bufferwriter = new BufferedWriter(filewrite);
				int i;
				for (i = 0; i < 10; i++) {
					bufferwriter.write(gf.random_string_create(9999));
					bufferwriter.write("\n");
				}
				bufferwriter.write(gf.random_string_create(2400));
				bufferwriter.close();
			}
			}
		    else if(name_folder.equals("1MB")){
			for (int k = 0; k < 100; k++) {
				new File("./" + name_folder).mkdirs();
				name_file = "1MB/" + gf.random_string_create(10) + ".txt";

				File file = new File(name_file);

				FileWriter filewrite = new FileWriter(file);
				BufferedWriter bufferwriter = new BufferedWriter(filewrite);
				int i;
				for (i = 0; i < 10; i++) {
					bufferwriter.write(gf.random_string_create(99999));
					bufferwriter.write("\n");
				}
				bufferwriter.write(gf.random_string_create(48576));
				bufferwriter.close();

			}
			}
		    else if(name_folder.equals("10MB")){
			for (int k = 0; k < 10; k++) {
				new File("./" + name_folder).mkdirs();
				name_file = "10MB/" + gf.random_string_create(10) + ".txt";

				File file = new File(name_file);

				FileWriter filewrite = new FileWriter(file);
				BufferedWriter bufferwriter = new BufferedWriter(filewrite);
				int i;
				for (i = 0; i < 10; i++) {
					bufferwriter.write(gf.random_string_create(999999));
					bufferwriter.write("\n");
				}
				bufferwriter.write(gf.random_string_create(485760));
				bufferwriter.close();
			}}
		    else if(name_folder.equals("100MB")){
			new File("./" + name_folder).mkdirs();
			name_file = "100MB/" + gf.random_string_create(10) + ".txt";

			File file = new File(name_file);

			FileWriter filewrite = new FileWriter(file);
			BufferedWriter bufferwriter = new BufferedWriter(filewrite);
			int i;
			for (i = 0; i < 10; i++) {
				bufferwriter.write(gf.random_string_create(9999999));
				bufferwriter.write("\n");
			}
			bufferwriter.write(gf.random_string_create(4857600));
			bufferwriter.close();
			}
		    else{
			System.out.println("Please provide input again");
		
		}

		System.out.println("All the files have been generated.");

	}

	public String random_string_create(int random_string_length) {
		StringBuffer randomString = new StringBuffer();
		for (int i = 0; i < random_string_length; i++) {
			int num = random_create_number();
			char character_l = CHARACTER_LIST.charAt(num);
			randomString.append(character_l);
		}
		return randomString.toString();
	}

	private static final String CHARACTER_LIST = "zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA0123456789";

	private int random_create_number() {
		int randomInteger = 0;
		Random randomGenerator = new Random();
		randomInteger = randomGenerator.nextInt(CHARACTER_LIST.length());
		if (randomInteger - 1 == -1) {
			return randomInteger;
		} else {
			return randomInteger - 1;
		}
	}

}