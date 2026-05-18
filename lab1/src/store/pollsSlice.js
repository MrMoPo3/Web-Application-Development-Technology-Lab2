import { createSlice, nanoid } from '@reduxjs/toolkit';

const initialState = {
  items: [
    {
      id: 'starter-poll',
      title: 'Який формат опитувань найзручніший для навчального проєкту?',
      description: 'Початкове демонстраційне опитування зі статистикою голосів.',
      options: [
        { id: 'single', text: 'Одне питання з варіантами', votes: 8 },
        { id: 'scale', text: 'Шкала оцінювання', votes: 5 },
        { id: 'open', text: 'Відкрита відповідь', votes: 3 },
      ],
      createdAt: '2026-05-18',
    },
  ],
};

const pollsSlice = createSlice({
  name: 'polls',
  initialState,
  reducers: {
    addPoll: {
      reducer(state, action) {
        state.items.unshift(action.payload);
      },
      prepare({ title, description, options }) {
        return {
          payload: {
            id: nanoid(),
            title,
            description,
            options: options.map((text) => ({
              id: nanoid(),
              text,
              votes: 0,
            })),
            createdAt: new Date().toISOString().slice(0, 10),
          },
        };
      },
    },
    addOption(state, action) {
      const poll = state.items.find((item) => item.id === action.payload.pollId);

      if (poll) {
        poll.options.push({
          id: nanoid(),
          text: action.payload.text,
          votes: 0,
        });
      }
    },
    vote(state, action) {
      const poll = state.items.find((item) => item.id === action.payload.pollId);
      const option = poll?.options.find((item) => item.id === action.payload.optionId);

      if (option) {
        option.votes += 1;
      }
    },
    removePoll(state, action) {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
  },
});

export const { addPoll, addOption, vote, removePoll } = pollsSlice.actions;
export default pollsSlice.reducer;
