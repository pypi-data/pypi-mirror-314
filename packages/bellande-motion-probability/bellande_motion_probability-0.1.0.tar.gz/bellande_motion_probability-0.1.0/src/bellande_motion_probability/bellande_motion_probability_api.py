# Copyright (C) 2024 Bellande Robotics Sensors Research Innovation Center, Ronaldson Bellande

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/env python3

import requests
import argparse
import json
import sys

def make_bellande_motion_probability_request(particle_state, previous_pose, current_pose, 
                                          noise_params=None, search_radius=50, sample_points=20):
    url = "https://bellande-robotics-sensors-research-innovation-center.org/api/Bellande_Motion_Probability/bellande_motion_probability"
    
    # Convert string inputs to lists if they're strings
    if isinstance(particle_state, str):
        particle_state = json.loads(particle_state)
    if isinstance(previous_pose, str):
        previous_pose = json.loads(previous_pose)
    if isinstance(current_pose, str):
        current_pose = json.loads(current_pose)
    if isinstance(noise_params, str):
        noise_params = json.loads(noise_params)
        
    payload = {
        "particle_state": particle_state,
        "previous_pose": previous_pose,
        "current_pose": current_pose,
        "noise_params": noise_params or {
            "trans_sigma": 0.1,
            "rot_sigma": 0.1,
            "head_sigma": 0.1
        },
        "search_radius": search_radius,
        "sample_points": sample_points,
        "auth": {
            "authorization_key": "bellande_web_api_opensource"
        }
    }
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error making request: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Run Bellande Motion Probability API")
    parser.add_argument("--particle-state", required=True, 
                       help="Current particle state as JSON-formatted list [x, y, heading, weight]")
    parser.add_argument("--previous-pose", required=True,
                       help="Previous pose as JSON-formatted list [x, y, heading]")
    parser.add_argument("--current-pose", required=True,
                       help="Current pose as JSON-formatted list [x, y, heading]")
    parser.add_argument("--noise-params",
                       help="Noise parameters as JSON object with trans_sigma, rot_sigma, and head_sigma")
    parser.add_argument("--search-radius", type=float, default=50.0,
                       help="Search radius for motion probability calculation")
    parser.add_argument("--sample-points", type=int, default=20,
                       help="Number of sample points for motion probability calculation")
    
    args = parser.parse_args()
    
    try:
        result = make_bellande_motion_probability_request(
            args.particle_state,
            args.previous_pose,
            args.current_pose,
            args.noise_params,
            args.search_radius,
            args.sample_points
        )
        
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in input parameters - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
