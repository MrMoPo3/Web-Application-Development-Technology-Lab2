export function selectCurrentUser(state) {
  return state.auth.users.find((user) => user.email === state.auth.currentUserEmail) ?? null;
}

export function getPollTotalVotes(poll) {
  return poll.options.reduce((sum, option) => sum + option.votes, 0);
}
