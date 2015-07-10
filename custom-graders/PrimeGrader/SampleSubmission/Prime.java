import java.io.IOException;
import java.util.Scanner;

public class Prime {

	public static void main(String args[]) throws IOException {
		Scanner in = new Scanner(System.in);
		String input;

		while (in.hasNextLine()) {
			input = in.nextLine();
			System.out.println(isPrime(Integer.parseInt(input)));
		}
	}

    public static Boolean isPrime(int num) {
        if (num == 2 ) return true;
        if (num % 2 == 0) return false;
        for (int i = 3; i * i <= num; i += 2)
            if (num % i == 0) return false;
        return true;
    }
}  