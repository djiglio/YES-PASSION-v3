import { supabase } from '../supabase.js';

export class DataLoader {
    static async loadSeason(seasonId) {
        try {
            let seasonStr = "";
            if (typeof seasonId === 'string' && seasonId.includes('-')) {
                seasonStr = seasonId;
            } else {
                let sNum = parseInt(seasonId);
                let startYear = 2000 + sNum - 1;
                seasonStr = `${startYear}-${startYear + 1}`;
            }

            console.log("Fetching data from Supabase for season:", seasonStr);
            
            const { data, error } = await supabase
                .from('players_history')
                .select('*')
                .eq('stagione', seasonStr)
                .eq('lega', 'Serie A')
                .limit(2000);

            if (error) {
                throw error;
            }

            if (!data || data.length === 0) {
                console.warn(`No data found for season ${seasonStr} in Serie A`);
                return null;
            }

            const parseValueNum = (valStr) => {
                if (!valStr) return 0;
                let num = parseFloat(valStr.replace(/[^0-9.]/g, ''));
                if (valStr.includes('M')) return num * 1000000;
                if (valStr.includes('K')) return num * 1000;
                return num;
            };

            const teamsMap = new Map();
            for (const p of data) {
                if (!teamsMap.has(p.squadra)) {
                    teamsMap.set(p.squadra, {
                        id: p.abbreviazione_squadra,
                        name: p.squadra,
                        abbr: p.abbreviazione_squadra,
                        real_points: 0,
                        squad_strength: 0,
                        players: []
                    });
                }
                
                // Formatta il ruolo separandolo con virgole se ha spazi, per compatibilit
                let roleFormatted = p.ruolo ? p.ruolo.split(' ').join(', ') : "";

                teamsMap.get(p.squadra).players.push({
                    Nome: p.nome_giocatore,
                    Ruolo: roleFormatted,
                    Overall: p.overall,
                    Potential: p.potenziale,
                    Value: p.valore_di_mercato,
                    ValueNum: parseValueNum(p.valore_di_mercato),
                    Age: parseInt(p.eta) || 0
                });
            }

            const teamsArray = Array.from(teamsMap.values());
            for (const team of teamsArray) {
                const sortedPlayers = [...team.players].sort((a, b) => b.Overall - a.Overall);
                const top11 = sortedPlayers.slice(0, 11);
                const sum = top11.reduce((acc, curr) => acc + curr.Overall, 0);
                team.squad_strength = Math.round(sum / (top11.length || 1));
            }

            return {
                season_id: seasonId.toString(),
                season_name: seasonStr,
                teams: teamsArray
            };

        } catch (error) {
            console.error("Error loading season data from Supabase:", error);
            return null;
        }
    }
}
