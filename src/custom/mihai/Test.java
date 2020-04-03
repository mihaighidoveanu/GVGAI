package custom.mihai;

import java.util.Random;

import core.logging.Logger;
import tools.Utils;
import tracks.ArcadeMachine;
import tools.ScoreLogger;
import java.text.SimpleDateFormat;
import java.io.IOException;

/**
 * Created with IntelliJ IDEA. User: Diego Date: 04/10/13 Time: 16:29 This is a
 * Java port from Tom Schaul's VGDL - https://github.com/schaul/py-vgdl
 */

public class Test {

    public static void main(String[] args) throws IOException {

		String customController = "custom.mihai.sampleMCTS.Agent";

		//Load available games
		String spGamesCollection =  "examples/all_games_sp.csv";
		String[][] games = Utils.readGames(spGamesCollection);

		//Game settings
		boolean visuals = true;
		int seed = new Random().nextInt();

		String recordActionsFile = null;// "actions_" + games[gameIdx] + "_lvl"
						// + levelIdx + "_" + seed + ".txt";
						// where to record the actions
						// executed. null if not to save.

		// 1. This starts a game, in a level, played by a human.
		// ArcadeMachine.playOneGame(game, level1, recordActionsFile, seed);

		//6. This plays N games, based on their index, in the first L levels, M times each. 
        //Actions to file optional (set saveActions to true). 
        //Logs to output/{experimentName}.

        int[] gamesIdx = new int[]{0};
        int N = gamesIdx.length, L = 1, M = 2;
        String experimentName = "test";
        String timeStamp = new SimpleDateFormat("MM.dd.HH.mm").format(new java.util.Date());
        String logFileName = "logs/" + experimentName + "_" + timeStamp + "_" + String.valueOf(L) + ".csv";

        ScoreLogger logger = new ScoreLogger(logFileName);
		boolean saveActions = false;
		String[] levels = new String[L];
		String[] actionFiles = new String[L*M];
        for (int i : gamesIdx) {
			int actionIdx = 0;
			String game = games[i][0];
			String gameName = games[i][1];
			for(int j = 0; j < L; ++j){
				levels[j] = game.replace(gameName, gameName + "_lvl" + j);
				if(saveActions) for(int k = 0; k < M; ++k)
				actionFiles[actionIdx++] = "actions_game_" + i + "_level_" + j + "_" + k + ".txt";
			}
            // send logger to ArcadeMachine, which logs a line for each game
			ArcadeMachine.runGames(game, levels, M, customController, saveActions? actionFiles:null, logger);
        }
        logger.write(); // actually writes to log file
    }
}
