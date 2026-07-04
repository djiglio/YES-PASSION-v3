import { DataLoader } from './js/data/DataLoader.js';

// Polyfill per fetch e supabase se necessari in ambiente Node (qui simuliamo fetch o vediamo se supabase-js in Node funge)
// Actually supabase is initialized with window.supabase in js/supabase.js, so Node.js will fail because window is undefined.
// Let's just create a quick stub or just rely on manual testing since it's front-end code.
