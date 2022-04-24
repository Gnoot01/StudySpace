const warriorsGames = [
  {
    awayTeam: {
      team: "Golden State",
      points: 119,
      isWinner: true,
    },
    homeTeam: {
      team: "Houston",
      points: 106,
      isWinner: false,
    },
  },
  {
    awayTeam: {
      team: "Golden State",
      points: 105,
      isWinner: false,
    },
    homeTeam: {
      team: "Houston",
      points: 127,
      isWinner: true,
    },
  },
  {
    homeTeam: {
      team: "Golden State",
      points: 126,
      isWinner: true,
    },
    awayTeam: {
      team: "Houston",
      points: 85,
      isWinner: false,
    },
  },
  {
    homeTeam: {
      team: "Golden State",
      points: 92,
      isWinner: false,
    },
    awayTeam: {
      team: "Houston",
      points: 95,
      isWinner: true,
    },
  },
  {
    awayTeam: {
      team: "Golden State",
      points: 94,
      isWinner: false,
    },
    homeTeam: {
      team: "Houston",
      points: 98,
      isWinner: true,
    },
  },
  {
    homeTeam: {
      team: "Golden State",
      points: 115,
      isWinner: true,
    },
    awayTeam: {
      team: "Houston",
      points: 86,
      isWinner: false,
    },
  },
  {
    awayTeam: {
      team: "Golden State",
      points: 101,
      isWinner: true,
    },
    homeTeam: {
      team: "Houston",
      points: 92,
      isWinner: false,
    },
  },
];

compareScores = ({awayTeam, homeTeam}, teamToSupport) => {
  const {team: aTeam, points: aPoints} = awayTeam;
  const {team: hTeam, points: hPoints} = homeTeam;
  scoreStatement =
    hPoints > aPoints
      ? `${aPoints}-<b>${hPoints}</b>`
      : `<b>${aPoints}</b>-${hPoints}`;
  const target = aTeam === teamToSupport ? awayTeam : homeTeam;
  return [`${aTeam} @ ${hTeam} ${scoreStatement}`, target.isWinner];
};

genTable = (supportTeam, games) => {
  const ul = document.createElement("ul");
  for (let game of games) {
    const result = document.createElement("li");
    [result.innerHTML, aWin] = compareScores(game, supportTeam);
    result.classList.add(aWin ? "won" : "loss");
    ul.append(result);
  }
  document.body.prepend(`From perspective of ${supportTeam}:`, ul);
};

genTable("Golden State", warriorsGames);
genTable("Houston", warriorsGames);

// From perspective of Golden State:
// if win, green li. Else, red li
// awayTeam @ homeTeam win(bolded)-lose
