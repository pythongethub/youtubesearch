import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.youtube.YouTube;
import com.google.api.services.youtube.model.SearchListResponse;
import com.google.api.services.youtube.model.SearchResult;

import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.security.GeneralSecurityException;

public class YouTubeDataAPI {

    private static final String APPLICATION_NAME = "YouTube Data API";
    private static final JacksonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();

    // Initialize YouTube API
    public static YouTube getService() throws GeneralSecurityException, IOException {
        return new YouTube.Builder(
            GoogleNetHttpTransport.newTrustedTransport(), JSON_FACTORY, null)
            .setApplicationName(APPLICATION_NAME)
            .build();
    }

    public static List<String> youtubeSearch(String query, int maxResults) throws IOException {
        YouTube youtube = getService();
        YouTube.Search.List search = youtube.search().list("id,snippet");
        search.setKey("YOUR_API_KEY"); // Replace with your actual API key
        search.setQ(query);
        search.setType("video");
        search.setOrder("viewCount");
        search.setMaxResults((long) maxResults);

        SearchListResponse searchResponse = search.execute();
        List<SearchResult> searchResultList = searchResponse.getItems();

        List<String> videoIds = new ArrayList<>();
        // ... Rest of the implementation to parse search results ...
        return videoIds;
    }

    public static void main(String[] args) throws GeneralSecurityException, IOException {
        // Example usage
        List<String> searchResults = youtubeSearch("query", 50);
        // ... Rest of the code to process and display results ...
    }
}
