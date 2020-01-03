import java.io.IOException;
import java.util.Scanner;

public class Factoring {

	public static void main(String args[]) throws IOException {
		Scanner in = new Scanner(System.in);
		String input;

		while (in.hasNextLine()) {
			input = in.nextLine();
			System.out.println(factor(Integer.parseInt(input)));
		}
	}

    public static String factor(int number) {
    	String factors = "";
    	
    	for(int factorNumber = 1; factorNumber <= number; factorNumber++){
            if(number % factorNumber == 0){
            	if (factorNumber != 1) {
            		factors += " ";
            	}
            	factors += factorNumber;
            }
        }
    	return factors;
    }
}